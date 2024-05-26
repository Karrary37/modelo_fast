from unittest.mock import patch

from fastapi.testclient import TestClient

from auth.adapters.api.api_auth import app

client = TestClient(app)


@patch('auth.domain.repositories.authenticate_user')
@patch('auth.domain.repositories.create_jwt')
def test_login_valid_credentials(mock_create_jwt_token, mock_authenticate_user):
    mock_authenticate_user.return_value = True
    mock_create_jwt_token.return_value = {'token': 'fake_token'}

    # Teste de credenciais válidas
    response = client.post(
        '/login', json={'username': 'user1', 'password': 'password1'}
    )

    assert response.status_code == 200


@patch('auth.domain.repositories.authenticate_user')
def test_login_invalid_credentials(mock_authenticate_user):
    mock_authenticate_user.return_value = False

    # Teste de credenciais inválidas
    response = client.post(
        '/login', json={'username': 'invalid_user', 'password': 'invalid_password'}
    )

    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid username or password'}


@patch('auth.domain.repositories.authenticate_user')
def test_login_missing_credentials(mock_authenticate_user):
    # Teste de credenciais ausentes
    response = client.post('/login', json={})

    assert response.status_code == 422  # Erro de validação do Pydantic
