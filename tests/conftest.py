from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from jwt import encode
from sqlalchemy import StaticPool, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from fastapi_zero.app import app
from fastapi_zero.database.database import get_session, table_registry
from fastapi_zero.models.user_model import User
from fastapi_zero.security import get_password_hash
from fastapi_zero.settings import Settings


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async with TestingSessionLocal() as db:
        try:
            yield db
        finally:
            await db.rollback()
            await db.close()

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)

    await engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 8, 16)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    password = 'teste123'
    user = User(
        username='Teste',
        email='teste@teste.com',
        password=get_password_hash(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def another_user(session):
    password = 'senha123'
    u = User(
        username='Alice',
        email='alice@test.com',
        password=get_password_hash(password),
    )
    session.add(u)
    session.commit()
    session.refresh(u)
    return u


@pytest.fixture
def token(client, user):
    response = client.post(
        '/login',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
def token_without_sub():
    token_data = {'foo': 'bar'}
    return encode(
        token_data, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )


@pytest.fixture
def token_invalid_email():
    token_data = {'sub': 'invalid@test.com'}

    return encode(
        token_data, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )
