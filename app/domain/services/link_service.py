import string
import random
from typing import Optional
from app.domain.models.link import Link
from app.domain.repositories.link_repository import LinkRepository

class LinkService:
    def __init__(self, repository: LinkRepository):
        self.repository = repository

    def shorten_url(self, original_url: str) -> Link:
        shortened_url = self.generate_shortened_url()
        link = Link(id=shortened_url, original_url=original_url, shortened_url=shortened_url)
        return self.repository.save_link(link)

    def get_original_url(self, shortened_url: str) -> Optional[Link]:
        return self.repository.get_link_by_shortened_url(shortened_url)

    def generate_shortened_url(self, length: int = 6) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
