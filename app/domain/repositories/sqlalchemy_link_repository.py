from typing import Optional

from sqlalchemy.orm import Session

from app.domain.models.link import LinkModel
from app.domain.repositories.link_repository import LinkRepository


class SQLAlchemyLinkRepository(LinkRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_link(self, link: LinkModel) -> LinkModel:
        db_link = LinkModel(
            id=link.id,
            original_url=str(link.original_url),
            shortened_url=link.shortened_url,
        )
        self.db.add(db_link)
        self.db.commit()
        self.db.refresh(db_link)
        return db_link

    def get_link_by_shortened_url(self, shortened_url: str) -> Optional[LinkModel]:
        return (
            self.db.query(LinkModel)
            .filter(LinkModel.shortened_url == shortened_url)
            .first()
        )
