import jwt

from auth.domain.repositories.create_jwt import create_jwt_token
from config import settings


def test_create_jwt_token_dict():
    username = 'test_user'
    token_data = create_jwt_token(username)

    assert isinstance(token_data, dict)


def test_create_jwt_token_return():
    username = 'user'
    token_data = create_jwt_token(username)

    assert 'token' in token_data
    assert 'expires_in' in token_data


def test_create_jwt_token_type_return():
    username = 'user1'
    token_data = create_jwt_token(username)

    assert isinstance(token_data['token'], str)
    assert isinstance(token_data['expires_in'], int)


def test_create_jwt_token_validity():
    username = 'valid_user'
    token_data = create_jwt_token(username)

    decoded_token = jwt.decode(
        token_data['token'], settings.APP_NAME, algorithms=['HS256']
    )

    assert 'sub' in decoded_token
    assert decoded_token['sub'] == username
