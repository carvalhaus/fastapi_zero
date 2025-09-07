from sqlalchemy.orm import Session

from fastapi_zero.repositories.user_repository import (
    create_user as create_user_repository,
)
from fastapi_zero.repositories.user_repository import (
    delete_user as delete_user_repository,
)
from fastapi_zero.repositories.user_repository import (
    get_user as get_user_repository,
)
from fastapi_zero.repositories.user_repository import (
    get_users as get_users_repository,
)
from fastapi_zero.repositories.user_repository import (
    update_user as update_user_repository,
)
from fastapi_zero.schemas.user_schema import UserSchema


def create_user(user: UserSchema, session: Session):
    return create_user_repository(user, session)


def get_users(session: Session, limit: int, offset: int):
    return get_users_repository(session, limit, offset)


def update_user(
    user_id: int, user: UserSchema, session: Session, current_user
):
    return update_user_repository(user_id, user, session, current_user)


def get_user(user_id: int, session: Session):
    return get_user_repository(user_id, session)


def delete_user(user_id: int, session: Session, current_user):
    return delete_user_repository(user_id, session, current_user)
