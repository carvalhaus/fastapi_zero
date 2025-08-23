from http import HTTPStatus

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

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    return create_user_controller(user, session)


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users(
    session: Session = Depends(get_session),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return get_users_controller(session, limit, offset)


@router.put(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    return update_user_controller(user_id, user, session)


@router.get(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int, session: Session = Depends(get_session)):
    return get_user_controller(user_id, session)


@router.delete(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    return delete_user_controller(user_id, session)
