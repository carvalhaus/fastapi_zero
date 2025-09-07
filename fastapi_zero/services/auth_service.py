from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.repositories.auth_repository import login as login_repository


async def login(form_data: OAuth2PasswordRequestForm, session: AsyncSession):
    return await login_repository(form_data, session)
