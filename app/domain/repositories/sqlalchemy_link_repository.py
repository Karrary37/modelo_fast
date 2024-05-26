from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.link import LinkModel
from app.domain.repositories.link_repository import LinkRepository

class SQLAlchemyLinkRepository(LinkRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_link(self, link: LinkModel) -> LinkModel:
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def get_link_by_shortened_url(self, shortened_url: str) -> Optional[LinkModel]:
        result = await self.db.execute(select(LinkModel).where(LinkModel.shortened_url == shortened_url))
        return result.scalars().first()
