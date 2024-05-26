from auth.domain.models.schemas_auth import AuthRequest, AuthResponse, TokenData


def test_auth_request_model():
    # Teste para verificar se a classe AuthRequest funciona corretamente
    auth_request_data = {'username': 'test_user', 'password': 'password123'}
    auth_request = AuthRequest(**auth_request_data)

    assert auth_request.username == auth_request_data['username']
    assert auth_request.password == auth_request_data['password']


def test_auth_response_model():
    # Teste para verificar se a classe AuthResponse funciona corretamente
    auth_response_data = {'token': 'fake_token_string'}
    auth_response = AuthResponse(**auth_response_data)

    assert auth_response.token == auth_response_data['token']


def test_token_data_model_with_username():
    # Teste para verificar se a classe TokenData funciona corretamente com um nome de usuário especificado
    username = 'test_user'
    token_data = TokenData(username=username)

    assert token_data.username == username


def test_token_data_model_without_username():
    # Teste para verificar se a classe TokenData funciona corretamente sem um nome de usuário especificado
    token_data = TokenData()

    assert token_data.username is None
