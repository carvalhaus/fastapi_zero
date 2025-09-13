from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.services.auth_service import login as login_service
from fastapi_zero.services.auth_service import (
    refresh_token as refresh_token_service,
)


async def login(form_data: OAuth2PasswordRequestForm, session: AsyncSession):
    return await login_service(form_data, session)


async def refresh_token(user):
    return await refresh_token_service(user)
