import logging.config

from fastapi import FastAPI

from app.adapters.api.fastapi_adapter import app as shorten_app
from auth import api as api_auth
from config import settings

app = FastAPI(title=settings.APP_NAME)

# Roteadores para as APIs
# app.include_router(app.router, prefix='/api', tags=['api'])
app.include_router(api_auth.router, prefix='/auth', tags=['auth'])

app.mount('/', shorten_app)

logger = logging.getLogger('check_log')
logger.info('Iniciando aplicação')
