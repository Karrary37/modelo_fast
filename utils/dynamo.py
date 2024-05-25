import json
import logging
import uuid
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key
import newrelic.agent
from fastapi import Response

from config import settings


class DynamoDBClient:
    """
    A client class for interacting with AWS DynamoDB.

    This class provides methods to interact with a specific DynamoDB table, including inserting items and handling conditional insertions.

    Attributes:
        table_name (str): The name of the DynamoDB table.
        dynamodb (resource): The DynamoDB resource object.
        table (Table): The DynamoDB Table resource.

    Methods:
        insert_item: Inserts an item into the DynamoDB table.
        insert_contract_dynamo: Inserts a contract into DynamoDB with conditional checks.
        insert_rejected_contract: Inserts a rejected contract into a specific DynamoDB table.
    """

    def __init__(self, table_name):
        """
        Initializes the DynamoDB client with a specified table name.

        Args:
            table_name (str): The name of the DynamoDB table to interact with.
        """
        self.logger = logging.getLogger('dynamoDB')
        self.table_name = table_name
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.table = self.dynamodb.Table(table_name)

    def insert_item(self, item):
        """
        Inserts an item into the DynamoDB table.

        Args:
            item (dict): The item to be inserted.

        Returns:
            Response: The response from the DynamoDB after attempting the insert.
        """
        try:
            response = self.table.put_item(Item=item)
            return response
        except Exception as e:
            newrelic.agent.notice_error()
            self.logger.error(f'Error inserting item: {e}')
            raise

    def insert_contract_dynamo(
        self, nuContratoCedente, cessionario, duplicity_hash, cedente
    ):
        """
         Inserts a new contract into the DynamoDB table with checks for duplicity.

        This function attempts to insert a contract into DynamoDB based on the provided hashes for duplicity
        and eligibility. It uses a conditional expression to ensure that duplicates are not inserted.

        Args:
            payload (dict): The contract data.
            duplicity_hash (str): The hash used for checking duplicity.

        Returns:
            Response: An HTTP response indicating the result of the operation.
        """
        item = {
            'ud_hash_contrato': duplicity_hash,
            'tx_nu_contrato': nuContratoCedente,
            'tx_nome_cedente': cedente,
            'tx_nome_cessionario': cessionario,
            'dt_data_insercao': datetime.now().isoformat(),
            'dt_data_atualizacao': None,
        }
        logger = logging.getLogger('duplicidade')
        try:
            self.table.put_item(
                Item=item, ConditionExpression='attribute_not_exists(ud_hash_contrato)'
            )
            logger.info(
                f'Contrato: {nuContratoCedente} | Contract approved in duplicity validation.'
            )
            return Response(status_code=200)
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            logger.info(
                f'Contrato: {nuContratoCedente} | Contract rejected in duplicity validation'
            )
            self.insert_rejected_contract(
                nuContratoCedente, cessionario, duplicity_hash, cedente
            )
            return Response(status_code=409)

    def insert_rejected_contract(
        self, nuContratoCedente, cessionario, duplicity_hash, cedente
    ):
        """
        Inserts a rejected contract into a specific table for tracking rejected contracts.

        This function is called when a contract insertion is rejected due to duplicity checks. It logs
        the rejected contract in a separate DynamoDB table designed for this purpose.

        Args:
            payload (dict): The data of the contract that was rejected.
            duplicity_hash (str): A hash representing the contract for duplicity checks.
            cedente (str): The name of the cedent of the contract.

        Returns:
            None: Indicates the operation was executed, errors are printed to the console.
        """
        rejected_table = self.dynamodb.Table('recusa_contrato')

        rejected_item = {
            'id': str(uuid.uuid4()),
            'ud_hash_contrato': duplicity_hash,
            'tx_nu_contrato': nuContratoCedente,
            'tx_nome_cedente': cedente,
            'en_motivo_recusa': 1,
            'tx_nome_cessionario': cessionario,
            'dt_data_recusa': datetime.now().isoformat(),
        }

        try:
            rejected_table.put_item(Item=rejected_item)
        except Exception as e:
            self.logger.warning(f'Error inserting rejected item: {e}')
            raise

    def delete_item(self, primary_key):
        """
        Delete a item from his primary key.
        """
        return self.table.delete_item(Key=primary_key)

    def insert_history_dynamo(
        self, nuContratoCedente, cessionario, duplicity_hash, type_history, cedente=None
    ):
        """
        Logs an action related to a contract into the DynamoDB for historical tracking.

        This function is designed to maintain a history of actions taken on contracts, such as insertions,
        rejections, and offers. It inserts a record into the DynamoDB table detailing the action taken.

        Args:
            payload (dict): The contract data.
            duplicity_hash (str): The hash used for checking duplicity.
            type_history:
            cedente:

        Returns:
            Response: An HTTP response indicating the result of the operation.

        """

        item = {
            'id': str(uuid.uuid4()),
            'ud_hash_contrato': duplicity_hash,
            'tx_nu_contrato': nuContratoCedente,
            'dt_data_historico': datetime.now().isoformat(),
            'en_acao': type_history,
            'tx_nome_cedente': cedente,
            'tx_nome_cessionario': cessionario,
        }
        try:
            self.table.put_item(Item=item)
            return Response(status_code=200)
        except Exception as e:
            newrelic.agent.notice_error()
            self.logger.warning(f'Error in save history contract: {e}')
            return Response(status_code=409)

    def offered_contract_dynamo(
        self, duplicity_hash, cedente, nu_contrato, cessionario=None
    ):
        """
        Offers a contract into DynamoDB, checking for duplicity in both 'contratos_ofertados' and 'inserir_contrato' tables.

        This method first checks for the contract in the 'detentor_contrato' table to see if it exists. If it does,
        and the current holder ('detentor') matches the 'cedente', it updates the holder to the new 'cessionario'.
        If the current holder does not match the 'cedente', it indicates a conflict. If no item is found, it suggests
        that the contract is not yet offered or recorded.

        Args:
            duplicity_hash (str): The hash used for checking duplicity of the contract.
            cedente (str): The current holder of the contract.
            cessionario (str, optional): The new proposed holder of the contract.
            nu_contrato (str, optional): The number of the contract.

        Returns:
            fastapi.Response: An HTTP response indicating the outcome. 200 if the holder was updated, 409 if there's a conflict with the current holder, 400 if the contract wasn't found, and 500 for any other errors.

        """

        try:
            response = self.table.get_item(Key={'ud_hash_contrato': duplicity_hash})
            if 'Item' in response:
                current_holder = str(response['Item']['tx_detentor']).lower()
                if current_holder == str(cedente).lower():
                    # Update the contract holder to the new assignee
                    self.update_contract_holder(duplicity_hash, cessionario)
                    self.logger.info(
                        f'Contract {nu_contrato} with hash {duplicity_hash} holder updated to {cessionario}'
                    )
                    response = {
                        'response': f'Contract {nu_contrato} with hash {duplicity_hash} holder updated to {cessionario}'
                    }
                    return Response(
                        status_code=200,
                        content=json.dumps(response),
                        media_type='application/json',
                    )
                else:
                    self.logger.error(
                        f'Contract {nu_contrato} with hash {duplicity_hash} the owner of the contract does not correspond to the information provided: {cedente}.'
                    )
                    response = {
                        'response': f'Contract {nu_contrato} with hash {duplicity_hash} the owner of the contract does not correspond to the information provided: {cedente}.'
                    }
                    return Response(
                        status_code=409,
                        content=json.dumps(response),
                        media_type='application/json',
                    )

            else:
                self.logger.warning(
                    f'Contract {nu_contrato} with hash {duplicity_hash} not found in table '
                    f'detentor_contrato.'
                )
                response = {
                    'response': f'Contract {nu_contrato} with hash {duplicity_hash} not found in table '
                    f'detentor_contrato.'
                }
                return Response(
                    status_code=400,
                    content=json.dumps(response),
                    media_type='application/json',
                )

        except Exception as e:
            newrelic.agent.notice_error()
            self.logger.error(f'Error querying contract holder: {e}')
            response = {'response': f'Error querying contract holder: {e}"'}
            return Response(
                status_code=500,
                content=json.dumps(response),
                media_type='application/json',
            )

    def get_user_by_username(self, username: str):
        """
        Search a user by id.

        Args:
            username (str): The id of user searched.

        Returns:
            dict: User if found, otherwise None.
        """
        try:
            response = self.table.get_item(Key={'tx_identificador': username})
            return response.get('Item')
        except Exception as e:
            newrelic.agent.notice_error()
            self.logger.warning(f'Error when searching for user: {e}')
            return None

    def update_contract_holder(self, duplicity_hash: str, holder: str):
        """
        Update table 'detentor_contrato' with a new holder.

        Args:
            duplicity_hash (str): The hash used for checking duplicity of the contract.
            holder (str, optional): The new proposed holder of the contract.
        """
        self.table.update_item(
            Key={'ud_hash_contrato': duplicity_hash},
            UpdateExpression='SET tx_detentor = :val1, dt_data_atualizacao = :val2',
            ExpressionAttributeValues={
                ':val1': holder,
                ':val2': datetime.now().isoformat(),
            },
        )

    def insert_contract_holder(
        self, duplicity_hash: str, cessionario: str, nu_contrato: str
    ):
        logger = logging.getLogger('save_contract_holder')
        item = {
            'ud_hash_contrato': duplicity_hash,
            'dt_data_atualizacao': datetime.now().isoformat(),
            'tx_detentor': cessionario,
            'tx_nu_contrato': nu_contrato,
        }
        try:
            self.table.put_item(Item=item)
            logger.info(
                f'Contrato {nu_contrato} salvo na detentor_contrato | Item {item}'
            )
            return Response(status_code=200)
        except Exception as e:
            logger.warning(
                f'Erro to save a contract {nu_contrato} in table detentor_contrato: {str(e)}'
            )
            newrelic.agent.notice_error()
            return Response(status_code=409)

    def get_history(
            self, duplicity_hash: str
    ):
        logger = logging.getLogger('get_history')
        response = self.table.query(IndexName="UdHashIndex", KeyConditionExpression=Key('ud_hash_contrato').eq(duplicity_hash))
        logger.info(f'History of contract {duplicity_hash}: {response}')
        return response
    