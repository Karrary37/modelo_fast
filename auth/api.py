from fastapi import APIRouter, Response

from .schemes import AuthReponse, AuthRequest

router = APIRouter()


@router.post('/login', response_model=AuthReponse)
def auth(body: AuthRequest):
    print(body.username)
    token = None
    if not token:
        return Response(status_code=401)

    return token
