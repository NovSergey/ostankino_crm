from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core.models import User

from .schemas import UserBase, UserEdit, UserChangePassword


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user: UserBase) -> User:
    check_user = await session.execute(select(User).where(User.username == user.username or User.phone == user.phone))
    if check_user.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User already exist")
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
    if user_exist and user_exist.check_password(user.password) and user_exist.is_active:
        return user_exist
    return None


async def delete_user(session: AsyncSession, username: str) -> bool:
    user = await get_user_by_username(session, username)
    if not user:
        return False
    user.is_active = False
    await session.commit()
    return True

async def edit_user(session: AsyncSession, username: str, user_edit: UserEdit) -> bool:
    user = await get_user_by_username(session, username)
    if not user:
        return False
    for name, value in user_edit.model_dump(exclude_unset=True).items():
        setattr(user, name, value)
    await session.commit()
    return True

async def change_password_user(session: AsyncSession, user_change: UserChangePassword) -> bool:
    user = await get_user_by_username(session, user_change.username)
    if not user:
        return False
    if not user.check_password(user_change.password):
        raise HTTPException(status_code=404, detail="Bad password")
    user.set_password(user_change.new_password)
    await session.commit()
    return True