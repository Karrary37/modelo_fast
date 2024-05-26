from sqlalchemy import Column, String
from app.database import Base
from pydantic import BaseModel, HttpUrl


class LinkModel(Base):
    __tablename__ = "links"

    id = Column(String, primary_key=True, index= True)
    original_url = Column(String, nullable=False)
    shortened_url = Column(String, unique=True, index=True, nullable=False)

class LinkBase(BaseModel):
    original_url: HttpUrl

class LinkCreate(LinkBase):
    pass

class LinkSchema(LinkBase):
    id: str
    shortened_url: str

    class Config:
        orm_mode = True
