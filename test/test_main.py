import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_app():
    response = client.get("/")
    assert response.status_code == 404  # Se não houver endpoint raiz
