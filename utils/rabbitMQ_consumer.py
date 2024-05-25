import json
import logging
import ssl

import newrelic.agent
import pika

from utils.dynamo import DynamoDBClient
from utils.hash import make_duplicity_hash
from utils.rabbitMQ_parameters import get_rabbitmq_parameters
from utils.rabbitMQ_roteador import Router


class RabbitMQConsumer:
    """
    Consumes messages from a specified RabbitMQ queue and processes them based on their type.
    This consumer handles messages by interacting with DynamoDB for data persistence and
    uses a Router for message forwarding based on business logic.
    """

    def __init__(self):
        """
        Initializes the consumer with the specified queue name and sets up RabbitMQ connection.
        """
        self.logger = logging.getLogger('consumer')
        self.setup_connection()

    def setup_connection(self):
        """Establishes connection to RabbitMQ server and declares the queue."""
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

            # Form the AMQPS URL
            parameters = get_rabbitmq_parameters()
            # Create connection parameters from the AMQPS URL

            # Establish connection and declare exchange
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.logger.info('Connection established successfully.')
        except Exception as e:
            newrelic.agent.notice_error()
            self.logger.error(f'Failed to establish connection: {e}')
            self.channel = None

    def start_consuming(self):
        """Establishes consuming to RabbitMQ server and declares the queue."""
        logger = logging.getLogger('consuming')
        function_queue_declare = {
            'duplicate_contract_queue': self.message_callback,
            'validate_eligibility_queue': self.validate_eligibility,
        }

        for queue, callback_funcion in function_queue_declare.items():
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.basic_consume(
                queue=queue,
                on_message_callback=callback_funcion,
                auto_ack=True,
            )

        if self.channel is None:
            logger.error(
                'Connection to RabbitMQ not established. It is not possible to start consuming.'
            )
            return

        self.logger.info('Starting message consumption.')
        self.channel.start_consuming()

    def validate_eligibility(self, ch, method, properties, body):
        logger = logging.getLogger('validate_eligibility')
        try:
            message = json.loads(body)
            logger.info(
                f"Consumindo validate_eligibility | {message['nuContratoFacta']}"
            )
            hash_duplicity = make_duplicity_hash(
                message['nuContratoFacta'], message['nuContratoCCB']
            )
            cessionario = message['cessionario']
            if message['statusElegibilidade']:
                type_history = 1
                holder_client = DynamoDBClient('detentor_contrato')
                holder_client.insert_contract_holder(
                    hash_duplicity, cessionario, message['nuContratoFacta']
                )

            else:
                type_history = 3
                insert_contract_client = DynamoDBClient('inserir_contrato')
                logger.info(
                    f'Contrato {message["nuContratoFacta"]} | Deleting from the table inserir_contrato'
                )
                insert_contract_client.delete_item({'ud_hash_contrato': hash_duplicity})

            history_client = DynamoDBClient('historico_contrato')
            history_client.insert_history_dynamo(
                message['nuContratoFacta'], cessionario, hash_duplicity, type_history
            )
        except Exception as err:
            newrelic.agent.notice_error()
            logger.warning(f'[Erro] validate_eligibility | {str(err)}')

    def message_callback(self, ch, method, properties, body):
        """
        Callback function to handle message processing.

        Decodes the message body, performs operations based on the message type,
        and routes the message if necessary.

        Args:
            ch (pika.channel.Channel): The channel object.
            method (pika.spec.Basic.Deliver): Delivery method.
            properties (pika.spec.BasicProperties): Message properties.
            body (bytes): The message body.
        """

        message = json.loads(body)
        operation_type = message.get('type')
        hash_duplicity = message.get('hash_duplicidade')
        hash_eligibility = message.get('hash_elegibilidade')
        cedente = message.get('cedente')
        payload = message.get('payload')

        dynamo_client_history = DynamoDBClient('historico_contrato')

        if operation_type == 'insert':
            logger = logging.getLogger('duplicidade')
            logger.info(
                f'Contrato: {payload["contrato"]["nuContratoCedente"]} | Start duplicity validation.'
            )
            self.handle_insert_operation(
                payload,
                hash_duplicity,
                hash_eligibility,
                cedente,
                dynamo_client_history,
            )

    def handle_insert_operation(
        self, payload, hash_duplicity, hash_eligibility, cedente, dynamo_client_history
    ):
        """
        Processes insert operation, inserts contract into DynamoDB, and routes message if successful.

        Args:
            payload (dict): Contract payload.
            hash_duplicity (str): Duplicity hash.
            hash_eligibility (str): Eligibility hash.
            cedente (str): Cedente information.
            dynamo_client_history (DynamoDBClient): DynamoDB client for history table.
        """
        dynamo_client = DynamoDBClient('inserir_contrato')
        response = dynamo_client.insert_contract_dynamo(
            payload['contrato']['nuContratoCedente'],
            payload['cessionario'],
            hash_duplicity,
            cedente,
        )
        if response.status_code == 200:
            self.process_response_and_route(
                payload,
                response,
                cedente,
                dynamo_client_history,
                hash_duplicity,
                operation_type=1,
            )

    def process_response_and_route(
        self,
        payload,
        response,
        cedente,
        dynamo_client_history,
        hash_duplicity,
        operation_type,
    ):
        """
        Processes the response from DynamoDB operations and routes the message accordingly.

        Args:
            payload (dict): Contract payload.
            response (Response): Response object from DynamoDB operation.
            cedente (str): Cedente information.
            dynamo_client_history (DynamoDBClient): DynamoDB client for history table.
            hash_duplicity (str): Duplicity hash.
            operation_type (int): Type of operation for history logging.
        """
        if response.status_code == 200:
            if payload:
                assignee = payload['cessionario']
                message_to_route = {'destiny': assignee, 'content': payload}
                router = Router()
                router.send_to_queue(message_to_route)
                router.close_connection()
            dynamo_client_history.insert_history_dynamo(
                payload['contrato']['nuContratoCedente'],
                payload['cessionario'],
                hash_duplicity,
                operation_type,
                cedente,
            )
        else:
            dynamo_client_history.insert_history_dynamo(
                payload['contrato']['nuContratoCedente'],
                payload['cessionario'],
                hash_duplicity,
                operation_type + 1,
                cedente,
            )
            self.logger.info('Error save history.')

    def close_connection(self):
        """Closes the RabbitMQ connection."""
        self.connection.close()
