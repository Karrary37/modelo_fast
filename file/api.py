from fastapi import APIRouter
from fastapi import Request

router = APIRouter()
jwt_protected_router = APIRouter()


@router.post('/teste')
async def teste(
        request: Request
):
    payload = await request.json()
    print(payload)
