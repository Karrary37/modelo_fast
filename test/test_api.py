import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import pytest
from httpx import AsyncClient
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.adapters.api.api_shorten import app as shorten_app
from tests.sqlite_link_repository import SQLiteLinkRepository, LinkModel

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()

@pytest.fixture
def app() -> FastAPI:
    return shorten_app

@pytest.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope='function')
def sqlite_db():
    engine = create_engine(DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()

    Base.metadata.drop_all(bind=engine)

def get_test_repository():
    return SQLiteLinkRepository(DATABASE_URL)

@pytest.fixture(scope='function', autouse=True)
def setup_dependencies(app: FastAPI, sqlite_db):
    app.dependency_overrides[Depends(get_test_repository)] = get_test_repository

@pytest.mark.asyncio
async def test_create_link(async_client: AsyncClient):
    response = await async_client.post(
        "/shorten/",
        json={"original_url": "http://example.com"}
    )
    assert response.status_code == 200
    assert "shortened_url" in response.json()

@pytest.mark.asyncio
async def test_redirect_to_original(async_client: AsyncClient):
    response = await async_client.post(
        "/shorten/",
        json={"original_url": "http://example.com"}
    )
    shortened_url = response.json()["shortened_url"].split("/")[-1]

    response = await async_client.get(f"/{shortened_url}/")
    assert response.status_code == 307
    assert response.headers["location"] == "http://example.com"
