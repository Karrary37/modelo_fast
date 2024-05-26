import asyncio
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Attr

from app.domain.models.schemas_link import LinkModel
from app.domain.repositories.link_repository import LinkRepository

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
)
table_name = 'links'
table = dynamodb.Table(table_name)


class DynamoDBLinkRepository(LinkRepository):
    async def save_link(self, link: LinkModel) -> LinkModel:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: table.put_item(
                Item={
                    'id': link.id,
                    'original_url': str(link.original_url),
                    'shortened_url': link.shortened_url,
                }
            ),
        )
        return link

    async def get_link_by_shortened_url(
        self, shortened_url: str
    ) -> Optional[LinkModel]:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: table.scan(
                FilterExpression=Attr('shortened_url').eq(shortened_url)
            ),
        )
        items = response.get('Items')
        if items:
            item = items[0]
            return LinkModel(
                id=item['id'],
                original_url=item['original_url'],
                shortened_url=item['shortened_url'],
            )
        return None


async def create_dynamodb_table():
    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    if table_name not in existing_tables:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 100, 'WriteCapacityUnits': 100},
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f'Table {table.table_name} created successfully.')
    else:
        print(f'Table {table_name} already exists.')
