from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from app.domain.models.link import Link
from app.domain.services.link_service import LinkService
from app.adapters.database.repository import InMemoryLinkRepository

app = FastAPI()
repository = InMemoryLinkRepository()
service = LinkService(repository)

class LinkCreateRequest(BaseModel):
    original_url: HttpUrl

@app.post("/shorten/", response_model=Link)
def create_link(request: LinkCreateRequest):
    link = service.shorten_url(request.original_url)
    return link

@app.get("/{shortened_url}", response_model=Link)
def redirect_to_original(shortened_url: str):
    link = service.get_original_url(shortened_url)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return link
