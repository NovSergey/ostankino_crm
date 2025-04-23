from authx.schema import TokenPayload
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .crud import get_user_by_username
from application.backend.core.config import security
from application.backend.core import db_helper
from application.backend.api.exceptions import RedirectException


async def check_user_permissions(session: AsyncSession, token_data: TokenPayload, need_superuser, redirect=False):
    username = token_data.sub
    if not username:
        if redirect:
            raise RedirectException("/login")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await get_user_by_username(session, username)
    if not user or not user.is_active:
        if redirect:
            raise RedirectException("/login")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unactive account")

    if not user.is_superuser and need_superuser:
        if redirect:
            raise RedirectException("/")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user


def check_current_user(need_superuser=False):
    async def dependency(
            session: AsyncSession = Depends(db_helper.session_dependency),
            token_data: TokenPayload = Depends(security.token_required())
    ):
        return await check_user_permissions(session, token_data, need_superuser)

    return dependency


def jwt_required_redirect(need_superuser=False):
    async def dependency(
            session: AsyncSession = Depends(db_helper.session_dependency),
            token_data: TokenPayload = Depends(security.token_required())
    ):
        await check_user_permissions(session, token_data, need_superuser, True)

    return dependency
