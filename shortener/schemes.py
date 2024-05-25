from pydantic import BaseModel


class ShortenerRequest(BaseModel):
    url: str
