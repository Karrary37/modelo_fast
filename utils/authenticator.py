from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt

from config import settings
from utils.dynamo import DynamoDBClient


class Authenticator:
    def __init__(self, dynamo_client: DynamoDBClient):
        self.dynamo_client = dynamo_client
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = 'HS256'
        self.access_token_expire_minutes = 15

    def verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.verify(password, hashed)

    def authenticate_user(self, username: str, password: str):
        user = self.dynamo_client.get_user_by_username(username)
        if user and self.verify_password(password, user['tx_hash_senha']):
            return user
        return False

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extracts and validates the current user from the JWT token.

    This function acts as a dependency for routes that require authentication. It decodes the JWT token provided in the request's Authorization header, using the secret key and the specified algorithm. The function then extracts the username (or user identifier) from the 'sub' claim of the token payload.

    If the token is valid and the 'sub' claim exists, the function returns the username, which can be used by the endpoint to perform further actions. If the token is invalid, expired, or the 'sub' claim is missing, it raises an HTTPException with a 401 status code, indicating that the credentials could not be validated.

    Args:
        token (str): The JWT token extracted from the Authorization header of the request.

    Raises:
        HTTPException: An exception with status code 401 (Unauthorized) if the token cannot be decoded, is invalid, or the 'sub' claim is missing.

    Returns:
        str: The username (or user identifier) extracted from the 'sub' claim of the JWT token, if the token is valid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
