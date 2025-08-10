from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from ..database.database import database
from ..schemas.user_schema import UserDB, UserList, UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)
    return user_with_id


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users():
    return {'users': database}


@router.put(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    database[user_id - 1] = user_with_id

    return user_with_id


@router.get(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    return database[user_id - 1]


@router.delete(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    return database.pop(user_id - 1)
