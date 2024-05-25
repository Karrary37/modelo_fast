from typing import Optional
from app.domain.models.link import Link
from app.domain.repositories.link_repository import LinkRepository

class InMemoryLinkRepository(LinkRepository):
    def __init__(self):
        self.links = {}

    def save_link(self, link: Link) -> Link:
        self.links[link.shortened_url] = link
        return link

    def get_link_by_shortened_url(self, shortened_url: str) -> Optional[Link]:
        return self.links.get(shortened_url)
