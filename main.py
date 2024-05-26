import logging.config
from fastapi import FastAPI
from app.adapters.api.fastapi_adapter import app as shorten_app
from auth import api as api_auth
from config import settings
from app.database import create_tables

app = FastAPI(title=settings.APP_NAME)

# Criar tabelas do banco de dados
create_tables()

# Roteadores para as APIs
app.include_router(api_auth.router, prefix='/auth', tags=['auth'])

# Incluindo roteador do encurtador de links
app.mount("/", shorten_app)

logger = logging.getLogger('check_log')
logger.info('Iniciando aplicação')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
