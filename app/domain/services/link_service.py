import random
import string
from typing import Optional

from app.domain.models.schemas_link import LinkModel
from app.domain.repositories.link_repository import LinkRepository


class LinkService:
    def __init__(self, repository: LinkRepository):
        self.repository = repository

    async def shorten_url(self, original_url: str) -> LinkModel:
        shortened_url = self.generate_shortened_url()
        link = LinkModel(
            id=shortened_url, original_url=original_url, shortened_url=shortened_url
        )
        return await self.repository.save_link(link)

    async def get_original_url(self, shortened_url: str) -> Optional[LinkModel]:
        return await self.repository.get_link_by_shortened_url(shortened_url)

    def generate_shortened_url(self, length: int = 6) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
