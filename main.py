import logging.config

from fastapi import FastAPI

from auth import api as api_auth
from config import settings
from shortener import api as api_file
from shortener.api import jwt_protected_router
from app.adapters.api.fastapi_adapter import app as shorten_app

app = FastAPI(title=settings.APP_NAME)

# Roteadores para as APIs
app.include_router(jwt_protected_router, prefix='/api', tags=['API Protegida por JWT'])
app.include_router(api_file.router, prefix='/api', tags=['api'])
app.include_router(api_auth.router, prefix='/auth', tags=['auth'])

app.mount("/", shorten_app)


# @app.get('/', include_in_schema=False)
# def read_root():
#     return {'status': 'Ok'}


logger = logging.getLogger('check_log')
logger.info("Iniciando aplicação")
