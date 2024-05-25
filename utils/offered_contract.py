import json
import logging

from fastapi import Response

from utils.define_routing_key import verify_routing_key
from utils.dynamo import DynamoDBClient
from utils.rabbitMQ_roteador import Router


def handle_offered_operation(
    payload, hash_duplicity, cedente, cessionario, dynamo_client_history
):
    """
    Processes offered operation, checks contract ownership, and routes message if conditions are met.

    Args:
        payload (dict): Contract payload.
        hash_duplicity (str): Duplicity hash.
        cedente (str): Cedente information.
        cessionario (str): Cessionario information.

    """
    assignee = payload['cessionario']
    cessionario_cadastrado = verify_routing_key(str(assignee))
    logger = logging.getLogger('oferta')
    if not cessionario_cadastrado:
        logger.warning(f'Cedente {assignee} is not registered')
        response = {'response': f'Cedente {assignee} is not registered"'}
        return Response(
            status_code=400, content=json.dumps(response), media_type='application/json'
        )
    dynamo_client = DynamoDBClient('detentor_contrato')
    nu_contrato = payload['contrato']['nuContratoCedente']
    response = dynamo_client.offered_contract_dynamo(
        hash_duplicity,
        cedente,
        nu_contrato,
        cessionario,
    )

    if response.status_code == 200:
        owner = payload['criado_por']
        payload['cedente'] = owner
        process_response_and_route(
            payload,
            response,
            cedente,
            dynamo_client_history,
            hash_duplicity,
            operation_type=1,
        )
        dynamo_client_history.insert_history_dynamo(
            payload['contrato']['nuContratoCedente'],
            payload['cessionario'],
            hash_duplicity,
            6,
            cedente,
        )
    return response


def process_response_and_route(
    payload,
    response,
    cedente,
    dynamo_client_history,
    hash_duplicity,
    operation_type,
):
    logger = logging.getLogger('oferta')
    """
    Processes the response from DynamoDB operations and routes the message accordingly.

    Args:
        payload (dict): Contract payload.
        response (Response): Response object from DynamoDB operation.
        cedente (str): Cedente information.
        dynamo_client_history (DynamoDBClient): DynamoDB client for history table.
        hash_duplicity (str): Duplicity hash.
        operation_type (int): Type of operation for history logging.
    """
    if response.status_code == 200:
        if payload:
            assignee = payload['cessionario']
            message_to_route = {'destiny': assignee, 'content': payload}
            router = Router()
            router.send_to_queue(message_to_route)
            router.close_connection()
        dynamo_client_history.insert_history_dynamo(
            payload['contrato']['nuContratoCedente'],
            payload['cessionario'],
            hash_duplicity,
            operation_type,
            cedente,
        )
    else:
        dynamo_client_history.insert_history_dynamo(
            payload['contrato']['nuContratoCedente'],
            payload['cessionario'],
            hash_duplicity,
            operation_type + 1,
            cedente,
        )
        logger.info('Error save history.')
