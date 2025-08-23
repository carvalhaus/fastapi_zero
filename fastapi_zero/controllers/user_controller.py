from sqlalchemy.orm import Session

from fastapi_zero.schemas.user_schema import UserSchema
from fastapi_zero.services.user_service import (
    create_user as create_user_service,
)
from fastapi_zero.services.user_service import get_users as get_users_service


def create_user(user: UserSchema, session: Session):
    return create_user_service(user, session)


def get_users(session: Session, limit: int, offset: int):
    return get_users_service(session, limit, offset)
