import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.adapters.api.api_shorten import app as shorten_app
import boto3
from botocore.exceptions import ClientError

@pytest.fixture
def app() -> FastAPI:
    return shorten_app

@pytest.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope='session')
def dynamodb_client():
    return boto3.client('dynamodb', region_name='us-east-1')

@pytest.fixture(scope='session')
def dynamodb_resource():
    return boto3.resource('dynamodb', region_name='us-east-1')

@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown_dynamodb_table(dynamodb_resource, dynamodb_client):
    table_name = 'links'

    # Create the table
    table = dynamodb_resource.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    yield

    # Delete the table
    table.delete()
    table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)

@pytest.mark.asyncio
async def test_create_link(async_client: AsyncClient):
    response = await async_client.post(
        "/shorten/",
        json={"original_url": "http://example.com"}
    )
    assert response.status_code == 200
    assert "shortened_url" in response.json()

@pytest.mark.asyncio
async def test_redirect_to_original(async_client: AsyncClient):
    # Primeiro, crie um link encurtado
    response = await async_client.post(
        "/shorten/",
        json={"original_url": "http://example.com"}
    )
    shortened_url = response.json()["shortened_url"].split("/")[-1]

    # Teste a redireção
    response = await async_client.get(f"/{shortened_url}/")
    assert response.status_code == 200
    assert response.headers["location"] == "http://example.com"
