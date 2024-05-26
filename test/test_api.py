import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.adapters.api.api_shorten import app as shorten_app
from app.domain.repositories.dynamodb_link_repository import create_dynamodb_table

@pytest.fixture
async def async_client():
    async with AsyncClient(app=shorten_app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_link(async_client):
    async with async_client as client:
        response = await client.post('/shorten/', json={"original_url": "https://example.com"})
        assert response.status_code == 200
        assert 'url_encurtado' in response.json()

@pytest.mark.asyncio
async def test_redirect_to_original(async_client):
    async with async_client as client:
        response = await client.post('/shorten/', json={"original_url": "https://example.com"})
        assert response.status_code == 200
        shortened_url = response.json()['url_encurtado'].split('/')[-1]

        redirect_response = await client.get(f'/{shortened_url}/', allow_redirects=False)
        assert redirect_response.status_code == 307
        assert redirect_response.headers['location'] == 'https://example.com'
