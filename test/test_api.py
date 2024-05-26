import pytest
from app.adapters.api.api_shorten import app as shorten_app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    with TestClient(shorten_app) as client:
        yield client

def test_create_link(client):
    response = client.post('/shorten/', json={"original_url": "https://example.com"})
    assert response.status_code == 200
    assert 'url_encurtado' in response.json()

def test_redirect_to_original(client):
    response = client.post('/shorten/', json={"original_url": "https://example.com"})
    assert response.status_code == 200
    shortened_url = response.json()['url_encurtado'].split('/')[-1]

    redirect_response = client.get(f'/{shortened_url}/', allow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers['location'] == 'https://example.com'
