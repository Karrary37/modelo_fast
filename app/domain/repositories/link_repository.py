from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.link import Link

class LinkRepository(ABC):
    @abstractmethod
    def save_link(self, link: Link) -> Link:
        pass

    @abstractmethod
    def get_link_by_shortened_url(self, shortened_url: str) -> Optional[Link]:
        pass
