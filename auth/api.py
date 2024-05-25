from fastapi import APIRouter, Response

from config import settings
from utils.cognito import Cognito

from .schemes import AuthReponse, AuthRequest

router = APIRouter()


@router.post('/login', response_model=AuthReponse)
def auth(body: AuthRequest):
    cgnt = Cognito(
        client_id=settings.COGNITO_CLIENT_ID, user_pool_id=settings.COGNITO_USER_POOL_ID
    )
    token = cgnt.login(username=body.username, password=body.password)
    if not token:
        return Response(status_code=401)

    return token
