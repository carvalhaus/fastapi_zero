from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.models.user_model import User
from fastapi_zero.security import create_access_token, verify_password


async def login(form_data: OAuth2PasswordRequestForm, session: AsyncSession):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token({'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


async def refresh_token(user):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}
