from sqlalchemy.orm import Session

from fastapi_zero.repositories.user_repository import (
    create_user as create_user_repository,
)
from fastapi_zero.repositories.user_repository import (
    get_users as get_users_repository,
)
from fastapi_zero.schemas.user_schema import UserSchema


def create_user(user: UserSchema, session: Session):
    return create_user_repository(user, session)


def get_users(session: Session, limit: int, offset: int):
    return get_users_repository(session, limit, offset)
