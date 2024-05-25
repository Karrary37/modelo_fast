import logging
import json

from fastapi import Response
from file.schemes.insert_attachments_contract_payload import InsertAttachmentsContractsPayload
from utils.define_routing_key import verify_routing_key
from utils.dynamo import DynamoDBClient
from utils.rabbitMQ_producer import RabbitMQProducer


def remove_none_from_payload(payload: dict):
    """
    Format payload recieved to insert attachments in the contract, removing 
    all keys with None values.
    """
    for anexo in payload['anexos']:
        keys_to_remove = []
        for key, value in anexo.items():
            if value is None:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            anexo.pop(key)
    return payload


def insert_contract_attachments(payload: InsertAttachmentsContractsPayload, duplicity_hash):
    """
    According to table historico_contrato, we send the attachment to the cedente and cessionario to all
    environments that have already received the contract.
    """  
    history_table = DynamoDBClient('historico_contrato')
    contract_history_details = history_table.get_history(duplicity_hash)
    if contract_history_details['Count'] == 0:
        return Response(
            status_code=404,
            content=json.dumps(
                {'response': f'Contract {payload.nuContratoCedente} not found.'}
                ),
            media_type='application/json'
            )

    contract_historys = contract_history_details["Items"]
    already_sent_environment = list()
    rabbitmq_producer = RabbitMQProducer('inserir_anexo')

    formatted_payload = remove_none_from_payload(payload.dict())

    for history in contract_historys:
        routing_key_cedente = history["tx_nome_cedente"]
        if routing_key_cedente not in already_sent_environment:    
            rabbitmq_producer.send_message(
                routing_key=routing_key_cedente,
                payload=formatted_payload
            )
            already_sent_environment.append(routing_key_cedente)
            logging.info(f'Enviando anexo para: {routing_key_cedente}')

        routing_key_cessionario = history["tx_nome_cessionario"]
        if routing_key_cessionario not in already_sent_environment:
            rabbitmq_producer.send_message(
                routing_key=routing_key_cessionario,
                payload=formatted_payload
            )
            already_sent_environment.append(routing_key_cessionario)
            logging.info(f'Enviando anexo para: {routing_key_cessionario}')
    
    return Response(
        status_code=200,
        content=json.dumps({
            'message': 'Inclusão de anexo realizada com sucesso.'
            }),
        media_type='application/json'
        )

