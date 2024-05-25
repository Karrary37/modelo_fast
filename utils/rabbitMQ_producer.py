import json
import logging
import ssl

import newrelic.agent
import pika

from utils.rabbitMQ_parameters import get_rabbitmq_parameters


class RabbitMQProducer:
    """
    A class responsible for producing and sending messages to a RabbitMQ exchange.
    This class establishes a connection with a RabbitMQ server and allows sending messages
    to a specified exchange. The exchange type is 'direct', meaning the messages are routed to queues based on the provided routing key.
    Attributes:
        connection (BlockingConnection): Connection to the RabbitMQ server.
        channel (Channel): Communication channel with RabbitMQ.
        exchange_name (str): Name of the exchange to which messages will be sent.
    Methods:
        send_message: Sends a message to the exchange with the specified routing key.
        close_connection: Closes the connection with the RabbitMQ server.
    """

    def __init__(self, exchange_name='contracts_exchange'):
        """
        Initializes the RabbitMQ producer by establishing a connection and declaring an exchange.
        """
        self.channel = None
        self.connection = None
        self.logger = logging.getLogger('consuming')
        self.exchange_name = exchange_name
        self.setup_connection()

    def setup_connection(self):
        """
        Establishes a secure connection to Amazon MQ using AMQPS and declares an exchange.
        """
        try:
            # Setup SSL context for secure connection
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

            parameters = get_rabbitmq_parameters()

            # Establish connection and declare exchange
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange=self.exchange_name, exchange_type='direct', durable=True
            )
            self.logger.info(
                'Producer connection to Amazon MQ established successfully.'
            )
        except Exception as e:
            newrelic.agent.notice_error()
            self.logger.error(
                f'Failed to establish producer connection to Amazon MQ: {e}'
            )
            self.channel = None

    def send_message(self, routing_key, payload):
        """
        Sends a JSON message to the specified RabbitMQ exchange using a routing key.
        """
        if self.channel is None:
            self.logger.info('Connection not established. Cannot send message.')
            return

        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close_connection(self):
        """
        Closes the connection to the RabbitMQ server.
        """
        if self.connection:
            self.connection.close()
            self.logger.info('Connection closed.')
