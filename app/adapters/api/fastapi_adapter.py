import logging
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.domain.repositories.sqlalchemy_link_repository import SQLAlchemyLinkRepository
from app.domain.services.link_service import LinkService
from auth.api import oauth2_scheme
from auth.verify_jwt import verify_jwt_token

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

async def get_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyLinkRepository:
    return SQLAlchemyLinkRepository(db)

async def get_service(repository: SQLAlchemyLinkRepository = Depends(get_repository)) -> LinkService:
    return LinkService(repository)

app = FastAPI()

class LinkCreateRequest(BaseModel):
    original_url: HttpUrl

class LinkCreateResponse(BaseModel):
    url_encurtado: str

@app.post('/shorten/', response_model=LinkCreateResponse)
async def create_link(
    request: LinkCreateRequest,
    request_obj: Request,
    service: LinkService = Depends(get_service),
    token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)
    link = await service.shorten_url(str(request.original_url))
    shortened_url = f'{request_obj.base_url}{link.shortened_url}'
    return {'url_encurtado': shortened_url}

@app.get('/{shortened_url}/')
async def redirect_to_original(
    shortened_url: str, service: LinkService = Depends(get_service)
):
    logger.info('Chamada ao endpoint de redirecionamento')
    link = await service.get_original_url(shortened_url)
    logger.info(f'Link encontrado: {link}')
    if link is None:
        logger.error('Link não encontrado')
        raise HTTPException(status_code=404, detail='Link not found')
    logger.info(f'Redirecionando para {link.original_url}')
    return RedirectResponse(url=link.original_url)
