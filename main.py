import logging.config

from fastapi import FastAPI

from auth import api as api_auth
from config import settings
from file import api as api_file
from file.api import jwt_protected_router

app = FastAPI(title=settings.APP_NAME)

# Roteadores para as APIs
app.include_router(jwt_protected_router, prefix='/api', tags=['API Protegida por JWT'])
app.include_router(api_file.router, prefix='/api', tags=['api'])
app.include_router(api_auth.router, prefix='/auth', tags=['auth'])


@app.get('/', include_in_schema=False)
def read_root():
    return {'status': 'Ok'}


logger = logging.getLogger('check_log')
logger.info("Iniciando aplicação")
