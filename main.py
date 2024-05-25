import logging.config

import newrelic.agent
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from auth import api as api_auth
from config import settings
from file import api as api_file
from file.api import jwt_protected_router
from file.consumidor import start_rabbitmq_consumer

if settings.IS_PROD:
    sentry_sdk.init(
        dsn='https://cb1fd25bacff4026862ef4e20a24f1d4@us.sentry.io/4506700195168256',
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    # newrelic.agent.initialize('newrelic.ini')
    # newrelic.agent.register_application()

# Configurações de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {'format': '{name} ({levelname}) :: {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'base'},
        'logtail': {
            'class': 'logtail.LogtailHandler',
            'formatter': 'base',
            'source_token': settings.LOG_TAIL_TOKEN,
        },
    },
    'loggers': {
        'esteira': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'oferta': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'duplicidade': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'validate_eligibility': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'consumer': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'consuming': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'save_contract_holder': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'app': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'producer': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'dynamoDB': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'roteador': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
        'get_history': {'handlers': ['console', 'logtail'], 'level': 'INFO'},
    },
}

logging.config.dictConfig(LOGGING)

app = FastAPI(title=settings.APP_NAME)

# Roteadores para as APIs
app.include_router(jwt_protected_router, prefix='/api', tags=['API Protegida por JWT'])
app.include_router(api_file.router, prefix='/api', tags=['api'])
app.include_router(api_auth.router, prefix='/auth', tags=['auth'])


@app.get('/', include_in_schema=False)
def read_root():
    return {'status': 'Ok'}


logger = logging.getLogger('app')
logger.info('Start app')


@app.on_event('startup')
async def startup_event():
    """
    Inicializa e inicia o consumidor do RabbitMQ no startup da aplicação.
    """
    from threading import Thread

    try:
        thread = Thread(target=start_rabbitmq_consumer)
        thread.start()
    except Exception as e:
        logger.error(f'Thread consumer error: {e}')
        newrelic.agent.notice_error()


@app.middleware('http')
async def exception_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.error(f'Erro inesperado: {e}')
        # Retorna uma resposta JSON indicando erro interno do servidor
        newrelic.agent.notice_error()
        return JSONResponse(
            content={'detail': 'Erro interno do servidor'}, status_code=500
        )
