from authx.schema import TokenPayload
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from application.backend.core.models import User
from application.backend.core.config import security
from application.backend.core import db_helper

from .schemas import UserBase


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user: UserBase) -> User:
    user_created = User(
        username=user.username,
        full_name=user.full_name,
        phone=user.phone,
    )
    user_created.set_password(user.password)
    session.add(user_created)
    await session.commit()
    return user_created


async def authenticate_user(session: AsyncSession, user: UserBase) -> User | None:
    user_exist = await get_user_by_username(session, user.username)
    if user_exist and user_exist.check_password(user.password):
        return user_exist
    return None


async def delete_user(session: AsyncSession, username: str) -> bool:
    user = await get_user_by_username(session, username)
    if not user:
        return False
    await session.delete(user)
    await session.commit()
    return True