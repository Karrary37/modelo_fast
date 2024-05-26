import pytest
from app.domain.models.schemas_link import LinkModel
from app.domain.services.link_service import LinkService
from app.domain.repositories.dynamodb_link_repository import DynamoDBLinkRepository

@pytest.fixture
def link_service():
    repository = DynamoDBLinkRepository()
    return LinkService(repository)

@pytest.mark.asyncio
async def test_shorten_url(link_service):
    original_url = 'https://example.com'
    link = await link_service.shorten_url(original_url)

    assert link is not None
    assert link.original_url == original_url
    assert len(link.shortened_url) == 6

@pytest.mark.asyncio
async def test_get_original_url(link_service):
    original_url = 'https://example.com'
    link = await link_service.shorten_url(original_url)

    fetched_link = await link_service.get_original_url(link.shortened_url)
    assert fetched_link is not None
    assert fetched_link.original_url == original_url
