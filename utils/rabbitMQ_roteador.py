import json
import ssl

import pika

from config import settings


class Router:
    """
    A class responsible for routing messages to a RabbitMQ exchange of the 'topic' type.

    This class establishes a connection with a RabbitMQ server and allows sending messages
    to a specified exchange. The exchange is of the 'topic' type, which allows for more flexible
    routing of messages based on route key patterns.

    Attributes:
        connection (BlockingConnection): Connection to the RabbitMQ server.
        channel (Channel): Communication channel with RabbitMQ.
        exchange_name (str): Name of the exchange to which the messages will be sent.

    Methods:
        send_to_queue: Sends a message to the exchange based on the route key determined by the payload.
        close_connection: Closes the connection with the RabbitMQ server.
    """

    def __init__(self):
        self.setup_connection()

    def setup_connection(self):
        """
        Establishes connection to Amazon MQ broker and declares the exchange.
        """
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
        self.exchange_name = 'roteador_contrato'
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type='topic', durable=True
        )

    def send_to_queue(self, payload):
        """
        Sends a message to a RabbitMQ exchange based on the route key derived from the payload.

        Args:
            payload (dict): The payload of the message to be sent, which includes the 'type' field to determine the route key.

        Returns:
            None
        """
        type = payload.get('destiny')
        routing_key = str(type)
        # Send the message to the exchange with the route key
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f'Message sent with route key {routing_key}')

    def close_connection(self):
        """
        Closes the connection to the RabbitMQ server.

        Returns:
            None
        """
        self.connection.close()
