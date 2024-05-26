from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth.authenticate_user import authenticate_user
from auth.create_jwt import create_jwt_token
from auth.schemes import AuthRequest, AuthResponse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/login', response_model=AuthResponse)
def login(auth_request: AuthRequest):
    print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
    username = auth_request.username
    password = auth_request.password
    if not authenticate_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
        )
    token_info = create_jwt_token(username)
    return token_info
