import jwt
import pytest
from fastapi import HTTPException, status

from auth.domain.models.schemas_auth import TokenData
from auth.domain.repositories.verify_jwt import verify_jwt_token
from config import settings


def test_verify_jwt_token_valid():
    username = 'test_user'
    token = jwt.encode({'sub': username}, settings.APP_NAME, algorithm='HS256')

    token_data = verify_jwt_token(token)

    assert isinstance(token_data, TokenData)
    assert token_data.username == username


def test_verify_jwt_token_expired():
    token = jwt.encode(
        {'sub': 'expired_user', 'exp': 0}, settings.APP_NAME, algorithm='HS256'
    )

    with pytest.raises(HTTPException) as e:
        verify_jwt_token(token)
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == 'Token expired'


def test_verify_jwt_token_invalid():
    token = 'invalid_token'

    with pytest.raises(HTTPException) as e:
        verify_jwt_token(token)
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == 'Invalid token'


def test_verify_jwt_token_missing_username():
    token = jwt.encode({}, settings.APP_NAME, algorithm='HS256')

    with pytest.raises(HTTPException) as e:
        verify_jwt_token(token)
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == 'Invalid token'
