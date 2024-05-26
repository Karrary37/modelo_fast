import logging.config
from fastapi import FastAPI
from app.adapters.api.fastapi_adapter import app as shorten_app
from auth import api as api_auth
from config import settings
from app.domain.repositories.dynamodb_link_repository import create_dynamodb_table

async def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # Criar a tabela DynamoDB
    await create_dynamodb_table()

    # Roteadores para as APIs
    app.include_router(api_auth.router, prefix='/auth', tags=['auth'])

    # Incluindo roteador do encurtador de links
    app.mount("/", shorten_app)

    logger = logging.getLogger('check_log')
    logger.info('Iniciando aplicação')

    return app

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app = await create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
