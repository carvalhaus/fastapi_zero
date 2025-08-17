from sqlalchemy.orm import Session

from fastapi_zero.schemas.user_schema import UserSchema
from fastapi_zero.services.user_service import (
    create_user as create_user_service,
)


def create_user(user: UserSchema, session: Session):
    return create_user_service(user, session)
