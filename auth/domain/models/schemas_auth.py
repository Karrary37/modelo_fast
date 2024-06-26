from typing import Optional

from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str


class TokenData(BaseModel):
    username: Optional[str] = None
