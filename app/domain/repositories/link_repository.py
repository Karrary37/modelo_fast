from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models.link import LinkModel


class LinkRepository(ABC):
    @abstractmethod
    def save_link(self, link: LinkModel) -> LinkModel:
        pass

    @abstractmethod
    def get_link_by_shortened_url(self, shortened_url: str) -> Optional[LinkModel]:
        pass
