from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth.domain.models.schemas_auth import AuthRequest, AuthResponse
from auth.domain.repositories.authenticate_user import authenticate_user
from auth.domain.repositories.create_jwt import create_jwt_token

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.post('/login', response_model=AuthResponse)
async def login(auth_request: AuthRequest):
    username = auth_request.username
    password = auth_request.password
    if not authenticate_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
        )
    token_info = create_jwt_token(username)
    return token_info
