from pydantic import BaseModel, HttpUrl

class Link(BaseModel):
    id: str
    original_url: HttpUrl
    shortened_url: str
