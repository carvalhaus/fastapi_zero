from http import HTTPStatus

from fastapi import APIRouter

from ..database.database import database
from ..schemas.user_schema import UserDB, UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)
    return user_with_id
