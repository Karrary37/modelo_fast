from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, HTTPException, status

from auth.schemes import AuthResponse, AuthRequest
from config import settings

router = APIRouter()

fake_db = {
    "user1": {
        "username": "user1",
        "password": "password1"
    },
    "user2": {
        "username": "user2",
        "password": "password2"
    }
}


def authenticate_user(username: str, password: str):
    user = fake_db.get(username)
    if not user or user["password"] != password:
        return False
    return True


def create_jwt_token(username: str) -> dict:
    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "sub": username,
        "exp": expiration_time.timestamp()
    }
    token = jwt.encode(payload, settings.APP_NAME, algorithm="HS256")
    return {"token": token, "expires_in": int((expiration_time - datetime.utcnow()).total_seconds())}


@router.post('/login', response_model=AuthResponse)
def login(auth_request: AuthRequest):
    username = auth_request.username
    password = auth_request.password
    if not authenticate_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token_info = create_jwt_token(username)
    print(token_info)
    return token_info
