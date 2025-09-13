from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.controllers.auth_controller import login as login_controller
from fastapi_zero.controllers.auth_controller import (
    refresh_token as refresh_token_controller,
)
from fastapi_zero.database.database import get_session
from fastapi_zero.schemas.auth_schema import Token
from fastapi_zero.security import get_current_user

router = APIRouter(tags=['Auth'])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
OAuthFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/login', response_model=Token)
async def login(
    session: SessionDep,
    form_data: OAuthFormDep,
):
    return await login_controller(form_data, session)


@router.post('/refresh_token', response_model=Token)
async def refresh_token(user=Depends(get_current_user)):
    return await refresh_token_controller(user)
