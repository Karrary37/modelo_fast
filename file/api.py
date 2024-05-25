from fastapi import APIRouter

from file.schemes import ShortenerRequest

router = APIRouter()
jwt_protected_router = APIRouter()


@router.post('/shortener')
async def shortener_link(
        body: ShortenerRequest
):
    print(body.url)
    return {"message": "OK"}
