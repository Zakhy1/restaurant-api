import asyncio
import os
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.databases import get_session
from app.main import app
from app.models import Base

dotenv_path = os.path.join(os.path.dirname(__file__), '../../test.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('POSTGRES_PORT')
# Подключение к БД
SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine_test = create_async_engine(url=SQLALCHEMY_DATABASE_URL)

async_session = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        yield ac
