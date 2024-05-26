import pytest
import boto3
from moto import mock_dynamodb
from app.domain.models.link import LinkModel
from app.domain.repositories.dynamodb_link_repository import DynamoDBLinkRepository, create_dynamodb_table

@pytest.fixture
def dynamodb_client():
     boto3.resource(
        'dynamodb',
        region_name='us-west-2',
    )

@pytest.fixture
def setup_dynamodb(dynamodb_client):
    create_dynamodb_table()

def test_save_and_get_link(dynamodb_client, setup_dynamodb):
    repository = DynamoDBLinkRepository()

    link = LinkModel(id='test_id', original_url='https://example.com', shortened_url='test_id')
    repository.save_link(link)

    fetched_link = repository.get_link_by_shortened_url('test_id')
    assert fetched_link is not None
    assert fetched_link.id == 'test_id'
    assert fetched_link.original_url == 'https://example.com'
    assert fetched_link.shortened_url == 'test_id'
