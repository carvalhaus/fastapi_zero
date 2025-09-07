from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_zero.controllers.auth_controller import login as login_controller
from fastapi_zero.database.database import get_session
from fastapi_zero.schemas.auth_schema import Token

router = APIRouter(tags=['Auth'])

SessionDep = Annotated[Session, Depends(get_session)]
OAuthFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/login', response_model=Token)
def login(
    session: SessionDep,
    form_data: OAuthFormDep,
):
    return login_controller(form_data, session)
