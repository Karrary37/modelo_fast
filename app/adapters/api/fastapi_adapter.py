from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from typing import List
from app.domain.models.link import Link
from app.domain.services.link_service import LinkService
from app.adapters.database.repository import InMemoryLinkRepository
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

repository = InMemoryLinkRepository()
service = LinkService(repository)

app = FastAPI()

class LinkCreateRequest(BaseModel):
    original_url: HttpUrl

class LinkCreateResponse(BaseModel):
    url_encurtado: str

@app.post("/shorten/", response_model=LinkCreateResponse)
def create_link(request: LinkCreateRequest, request_obj: Request):
    logger.info('Chamada ao endpoint de redirecionamento')
    link = service.shorten_url(request.original_url)
    shortened_url = f"{request_obj.base_url}{link.shortened_url}"
    return {"url_encurtado": shortened_url}

@app.get("/{shortened_url}/")
def redirect_to_original(shortened_url: str):
    logger.info('Chamada ao endpoint de redirecionamento')
    link = service.get_original_url(shortened_url)
    logger.info(f'Link encontrado: {link}')
    if link is None:
        logger.error('Link não encontrado')
        raise HTTPException(status_code=404, detail="Link not found aaaaaaaaaaaaa")
    logger.info(f'Redirecionando para {link.original_url}')
    return RedirectResponse(url=link.original_url)

@app.get('src/batata/')
def batata():
    return {'msg': 'batata'}
