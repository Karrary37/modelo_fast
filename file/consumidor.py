import logging

from fastapi import FastAPI

from utils.rabbitMQ_consumer import RabbitMQConsumer

app = FastAPI()
logger = logging.getLogger(__name__)


def start_rabbitmq_consumer():
    """
    Initializes and starts the RabbitMQ consumer.

    This function creates an instance of the RabbitMQConsumer class and starts consuming messages
    from the 'duplicate_contract_queue'. It's designed to be called during the startup of the FastAPI application.
    """
    consumer = RabbitMQConsumer()
    consumer.start_consuming()
