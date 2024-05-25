
from fastapi import APIRouter

router = APIRouter()
jwt_protected_router = APIRouter()


@router.post('/teste')
async def send_contract(
):
    print('---------------------')

