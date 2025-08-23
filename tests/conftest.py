from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import sessionmaker

from fastapi_zero.app import app
from fastapi_zero.database.database import get_session, table_registry
from fastapi_zero.models.user_model import User


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        table_registry.metadata.drop_all(engine)
        engine.dispose()


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


@pytest.fixture
def user(session):
    user = User(username='Teste', email='teste@teste.com', password='teste123')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
