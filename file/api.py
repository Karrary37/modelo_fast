import json
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status

from file.schemes import ValidationPayload
from file.schemes.authenticator_payload import LoginData
from file.schemes.insert_attachments_contract_payload import InsertAttachmentsContractsPayload
from file.insert_attachments.insert_contract_attachments import insert_contract_attachments
from utils.authenticator import Authenticator, get_current_user
from utils.dynamo import DynamoDBClient
from utils.hash import generate_hash, generate_hash_oferta, make_duplicity_hash
from utils.offered_contract import handle_offered_operation
from utils.process_payload import process_payload
from utils.rabbitMQ_producer import RabbitMQProducer

router = APIRouter()
jwt_protected_router = APIRouter()


@jwt_protected_router.post('/enviar_contrato')
async def send_contract(
    payload: ValidationPayload, current_user: str = Depends(get_current_user)
):
    """
    Receives a contract payload, generates duplicity and eligibility hashes, and sends it to a RabbitMQ queue.

    This API route receives a contract payload, generates specific hashes to check for duplicity and eligibility,
    and then publishes a message with this information to a RabbitMQ queue for future processing.

    Args:
        payload (ValidationPayload): A payload object containing the contract data.

    Returns:
        dict: A dictionary with the operation status.
        current_user: A authenticator jwt.
    """

    logger = logging.getLogger('esteira')
    logger.info('Start contract insertion')
    duplicity_hash, eligibility_hash = generate_hash(payload)

    beneficio = payload.beneficio
    if beneficio is None:
        payload.beneficio = {}

    contratos_origem = payload.contratosOrigem
    if contratos_origem is None:
        payload.contratosOrigem = []

    data = process_payload(payload)
    data['cedente'] = current_user

    rabbitmq_producer = RabbitMQProducer()
    message = {
        'payload': data,
        'hash_duplicidade': duplicity_hash,
        'hash_elegibilidade': eligibility_hash,
        'type': 'insert',
        'cedente': 'facta',
    }

    rabbitmq_producer.send_message('duplicate_contract_queue', message)
    rabbitmq_producer.close_connection()

    response = {'status': 'Contract successfully received'}
    return Response(
        status_code=200, content=json.dumps(response), media_type='application/json'
    )


@jwt_protected_router.post('/ofertar_contrato')
async def offered_contract(payload: dict, bt: BackgroundTasks):
    """
    Offers a contract based on the provided payload.

    This API route is responsible for receiving a contract payload, generating duplicity and eligibility hashes,
    and preparing a response containing these hashes and a success message.

    Args:
        payload (ValidationPayload): A payload object containing the contract data.
        bt (BackgroundTasks): Tasks to be executed in the background (currently not used).

    Returns:
        Response: An HTTP response with the operation status and the generated hashes.
        Response: An HTTP response with the operation status and the generated hashes.
    """
    duplicity_hash, eligibility_hash = generate_hash_oferta(payload)
    cedente = payload.get('cedente')
    cessionario = payload.get('cessionario')
    dynamo_client_history = DynamoDBClient('historico_contrato')
    response = handle_offered_operation(
        payload, duplicity_hash, cedente, cessionario, dynamo_client_history
    )
    return response


@router.post('/token')
async def login_for_access_token(form_data: LoginData):
    """
    Authenticates a user based on provided credentials and generates a JWT token.

    This authentication endpoint verifies the user's credentials against the records in the DynamoDB database. Upon successful authentication, a JWT token is generated and returned to the user. This token is required to access protected API routes that require authentication.

    Args:
        form_data (LoginData): A Pydantic object containing 'username' and 'password' provided by the user.

    Raises:
        HTTPException: An exception is raised with a 401 (Unauthorized) status if the provided credentials are incorrect or cannot be validated.

    Returns:
        dict: A dictionary containing the generated 'access_token' and the 'token_type', which is typically "bearer".
    """
    dynamo_client = DynamoDBClient('usuarios_roteador')
    authenticator = Authenticator(dynamo_client)
    user = authenticator.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = authenticator.create_access_token(
        data={'sub': user['tx_identificador']}
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@jwt_protected_router.post('/inserir-anexo-contrato')
async def insert_contract_attachment(
    payload: InsertAttachmentsContractsPayload, current_user: str = Depends(get_current_user)
    ):
    """
    Inserts an attachment in all enviroments that a contract has been based on the provided payload.
    """
    duplicity_hash = make_duplicity_hash(payload.nuContratoCedente, payload.nuContratoCCB)
    response = insert_contract_attachments(payload, duplicity_hash)
    return response
