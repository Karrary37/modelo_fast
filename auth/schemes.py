from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthReponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class User(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = None


# class UserRegister(BaseModel):
#     username: str
#     password: str
#     full_name: str | None = None
#     disabled: bool | None = None
#     provider_pix: str


class UserInDB(User):
    sub: str
    provider_pix: str
    extra_data: dict
