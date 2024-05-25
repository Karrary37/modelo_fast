from functools import lru_cache

from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = 'Awesome API'
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    COGNITO_CLIENT_ID: str
    COGNITO_USER_POOL_ID: str
    S3_BUCKET_NAME: str
    S3_CUSTOM_DOMAIN: str
    AWS_URL_RABBIT: str
    AWS_USER_RABBIT: str
    AWS_PASSWORD_RABBIT: str
    IS_PROD: bool
    JWT_SECRET_KEY: str
    LOG_TAIL_TOKEN: str
    URL_RABBIT_LOCAL: str
    IS_LOCAl: bool
    ROUTING_KEYS: str


@lru_cache()
def _get_settings():
    return Settings(
        APP_NAME=config('APP_NAME'),
        AWS_REGION=config('AWS_REGION'),
        AWS_ACCESS_KEY_ID=config('AWS_ACCESS_KEY_ID'),
        AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY'),
        S3_BUCKET_NAME=config('S3_BUCKET_NAME'),
        S3_CUSTOM_DOMAIN=config('S3_CUSTOM_DOMAIN'),
        COGNITO_CLIENT_ID=config('COGNITO_CLIENT_ID'),
        COGNITO_USER_POOL_ID=config('COGNITO_USER_POOL_ID'),
        AWS_URL_RABBIT=config('AWS_URL_RABBIT'),
        AWS_USER_RABBIT=config('AWS_USER_RABBIT'),
        AWS_PASSWORD_RABBIT=config('AWS_PASSWORD_RABBIT'),
        IS_PROD=config('IS_PROD'),
        JWT_SECRET_KEY=config('JWT_SECRET_KEY'),
        LOG_TAIL_TOKEN=config('LOG_TAIL_TOKEN'),
        URL_RABBIT_LOCAL=config('URL_RABBIT_LOCAL'),
        IS_LOCAl=config('IS_LOCAl'),
        ROUTING_KEYS=config('ROUTING_KEYS'),
    )
settings = _get_settings()
