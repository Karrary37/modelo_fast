from fastapi import HTTPException, Request


async def is_authenticated(request: Request):
    if not request.state.user:
        raise HTTPException(status_code=401)
