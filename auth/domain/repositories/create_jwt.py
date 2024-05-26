from datetime import datetime, timedelta

import jwt

from config import settings


def create_jwt_token(username: str) -> dict:
    expiration_time = datetime.utcnow() + timedelta(minutes=15)
    payload = {'sub': username, 'exp': expiration_time.timestamp()}
    token = jwt.encode(payload, settings.APP_NAME, algorithm='HS256')
    return {
        'token': token,
        'expires_in': int((expiration_time - datetime.utcnow()).total_seconds()),
    }
