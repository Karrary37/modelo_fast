import ssl

import certifi
import pika

from config import settings


def get_rabbitmq_parameters():
    """
    Generates and returns the connection parameters for RabbitMQ based on the environment.

    This function checks if the application is running in a local environment or not.
    For a local environment, it uses the RabbitMQ URL defined in the local settings.
    For a production environment, it constructs an AMQPS URL using AWS credentials and settings,
    and sets up SSL options with a CA certificate file from certifi.

    Returns:
        pika.URLParameters: The connection parameters for RabbitMQ, including SSL configuration
                            for production environments.
    """
    # Checks if it is in a local environment or not
    if settings.IS_LOCAl:
        # Configuration for a local environment
        amqp_url = settings.URL_RABBIT_LOCAL
        parameters = pika.URLParameters(amqp_url)
    else:
        # Constructs the AMQPS URL for the production environment
        amqps_url = (
            f'amqps://{settings.AWS_USER_RABBIT}:{settings.AWS_PASSWORD_RABBIT}'
            f'@{settings.AWS_URL_RABBIT}.mq.{settings.AWS_REGION}.amazonaws.com:5671'
        )
        parameters = pika.URLParameters(amqps_url)
        ssl_context = ssl.create_default_context(
            cafile=certifi.where()
        )  # Defines the SSL context if necessary
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

    return parameters
