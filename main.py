import logging.config

from fastapi import FastAPI

from app.adapters.api.api_shorten import app as shorten_app
from app.domain.repositories.dynamodb_link_repository import create_dynamodb_table
from auth.adapters.api.api_auth import app as auth_app
from config import settings


async def create_app() -> FastAPI:
    await create_dynamodb_table()

    logger = logging.getLogger('check_log')
    logger.info('Iniciando aplicação')

    return app


app = FastAPI(title=settings.APP_NAME)

app.mount('/auth', auth_app)
app.mount('/', shorten_app)


@app.on_event('startup')
async def startup_event():
    await create_app()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
