from functools import lru_cache

from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    SECRET_KEY: str


@lru_cache()
def _get_settings():
    return Settings(
        APP_NAME=config('APP_NAME'),
        SECRET_KEY=config('SECRET_KEY'),
    )


settings = _get_settings()
