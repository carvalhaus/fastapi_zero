from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from fastapi_zero.settings import Settings

table_registry = registry()

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
