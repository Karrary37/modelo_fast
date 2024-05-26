from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./shorten-database.db"

# Async engine para operações assíncronas
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False, "timeout": 30}  # Adicionando timeout
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
Base = declarative_base()

# Synchronous engine para criação de tabelas
sync_engine = create_engine(
    "sqlite:///./shorten-database.db",
    connect_args={"check_same_thread": False, "timeout": 30}  # Adicionando timeout
)

def create_tables():
    Base.metadata.create_all(bind=sync_engine)
