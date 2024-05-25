from fastapi import Request
from fastapi.responses import Response

from config import settings
from utils.cognito import Cognito


async def needs_auth(request: Request, call_next):
    try:
        access_token = request.headers.get('Authorization')
        user = None
        if access_token:
            cgnt = Cognito(
                client_id=settings.COGNITO_CLIENT_ID,
                user_pool_id=settings.COGNITO_USER_POOL_ID,
            )
            user = cgnt.get_user(token=access_token)

        request.state.user = user
        return await call_next(request)

    except Exception as e:
        return Response(status_code=500, content=str(e))
