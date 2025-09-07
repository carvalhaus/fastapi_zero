from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.services.auth_service import login as login_service


async def login(form_data: OAuth2PasswordRequestForm, session: AsyncSession):
    return await login_service(form_data, session)
