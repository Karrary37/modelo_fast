import pytest

from auth.domain.repositories import fake_db as db
from auth.domain.repositories.authenticate_user import authenticate_user


# Fixture para configurar o ambiente de teste
@pytest.fixture
def setup_fake_db():
    # Configurar o banco de dados falso com alguns usuários de exemplo
    db.fake_db = {
        'alice': {'username': 'alice', 'password': 'wonderland'},
        'bob': {'username': 'bob', 'password': 'builder'},
        'charlie': {'username': 'charlie', 'password': 'chocolate'}
    }


# Teste para verificar se a autenticação funciona corretamente para um usuário existente
def test_authenticate_user_valid(setup_fake_db):
    assert authenticate_user('alice', 'wonderland') == True


# Teste para verificar se a autenticação falha para um usuário inexistente
def test_authenticate_user_invalid_username(setup_fake_db):
    assert authenticate_user('eve', 'unknown') == False


# Teste para verificar se a autenticação falha para um usuário existente com senha incorreta
def test_authenticate_user_invalid_password(setup_fake_db):
    assert authenticate_user('bob', 'incorrect') == False


# Teste para verificar se a autenticação falha quando o usuário está vazio
def test_authenticate_user_empty_username(setup_fake_db):
    assert authenticate_user('', 'password') == False


# Teste para verificar se a autenticação falha quando a senha está vazia
def test_authenticate_user_empty_password(setup_fake_db):
    assert authenticate_user('charlie', '') == False


# Teste para verificar se a autenticação falha quando ambos o usuário e a senha estão vazios
def test_authenticate_user_empty_credentials(setup_fake_db):
    assert authenticate_user('', '') == False
