from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from fastapi_zero.controllers.user_controller import (
    create_user as create_user_controller,
)
from fastapi_zero.controllers.user_controller import (
    delete_user as delete_user_controller,
)
from fastapi_zero.controllers.user_controller import (
    get_user as get_user_controller,
)
from fastapi_zero.controllers.user_controller import (
    get_users as get_users_controller,
)
from fastapi_zero.controllers.user_controller import (
    update_user as update_user_controller,
)
from fastapi_zero.database.database import get_session
from fastapi_zero.schemas.message_schema import Message
from fastapi_zero.schemas.user_schema import (
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_zero.security import get_current_user

router = APIRouter(prefix='/users', tags=['Users'])

SessionDep = Annotated[Session, Depends(get_session)]
LimitDep = Annotated[int, Query(ge=1, le=100)]
OffsetDep = Annotated[int, Query(ge=0)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: SessionDep):
    return create_user_controller(user, session)


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users(
    session: SessionDep,
    limit: LimitDep = 10,
    offset: OffsetDep = 0,
    current_user=Depends(get_current_user),
):
    return get_users_controller(session, limit, offset)


@router.put(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    return update_user_controller(user_id, user, session, current_user)


@router.get(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int, session: SessionDep):
    return get_user_controller(user_id, session)


@router.delete(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(
    user_id: int,
    session: SessionDep,
    current_user=Depends(get_current_user),
):
    return delete_user_controller(user_id, session, current_user)
