from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.repositories.user_repository import (
    create_user as create_user_repository,
)
from fastapi_zero.repositories.user_repository import (
    delete_user as delete_user_repository,
)
from fastapi_zero.repositories.user_repository import (
    get_user as get_user_repository,
)
from fastapi_zero.repositories.user_repository import (
    get_users as get_users_repository,
)
from fastapi_zero.repositories.user_repository import (
    update_user as update_user_repository,
)
from fastapi_zero.schemas.user_schema import UserSchema


async def create_user(user: UserSchema, session: AsyncSession):
    return await create_user_repository(user, session)


async def get_users(session: AsyncSession, limit: int, offset: int):
    return await get_users_repository(session, limit, offset)


async def update_user(
    user_id: int, user: UserSchema, session: AsyncSession, current_user
):
    return await update_user_repository(user_id, user, session, current_user)


async def get_user(user_id: int, session: AsyncSession):
    return await get_user_repository(user_id, session)


async def delete_user(user_id: int, session: AsyncSession, current_user):
    return await delete_user_repository(user_id, session, current_user)
