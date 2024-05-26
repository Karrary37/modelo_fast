import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_app():
    response = client.get("/")
    assert response.status_code == 404  # Se não houver endpoint raiz
