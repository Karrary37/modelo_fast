import json
import ssl

import pika

from config import settings


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

    def __init__(self):
        """
        Initializes the RabbitMQ producer by establishing a connection and declaring an exchange.
        """
        self.exchange_name = 'contracts_exchange'
        self.setup_connection()

    def setup_connection(self):
        """
        Establishes a secure connection to Amazon MQ using AMQPS and declares an exchange.
        """
        try:
            # Setup SSL context for secure connection
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

            # Form the AMQPS URL
            amqps_url = (
                f'amqps://{settings.AWS_USER_RABBIT}:{settings.AWS_PASSWORD_RABBIT}'
                f'@{settings.AWS_URL_RABBIT}.mq.{settings.AWS_REGION}.amazonaws.com:5671'
            )

            # Create connection parameters from the AMQPS URL
            parameters = pika.URLParameters(amqps_url)
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)

            # Establish connection and declare exchange
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange=self.exchange_name, exchange_type='direct', durable=True
            )
            print('Producer connection to Amazon MQ established successfully.')
        except Exception as e:
            print(f'Failed to establish producer connection to Amazon MQ: {e}')
            self.channel = None

    def send_message(self, routing_key, payload):
        """
        Sends a JSON message to the specified RabbitMQ exchange using a routing key.
        """
        if self.channel is None:
            print('Connection not established. Cannot send message.')
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
            print('Connection closed.')
