from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class LinkModel(Base):
    __tablename__ = 'links'

    id = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    shortened_url = Column(String, unique=True, index=True, nullable=False)

class SQLiteLinkRepository:
    def __init__(self, db_url='sqlite:///./test.db'):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def save_link(self, link: LinkModel) -> LinkModel:
        db = self.SessionLocal()
        db.add(link)
        db.commit()
        db.refresh(link)
        db.close()
        return link

    def get_link_by_shortened_url(self, shortened_url: str) -> LinkModel:
        db = self.SessionLocal()
        link = db.query(LinkModel).filter(LinkModel.shortened_url == shortened_url).first()
        db.close()
        return link
