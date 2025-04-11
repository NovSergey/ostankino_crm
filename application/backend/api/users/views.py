from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from application.backend.core import db_helper
from . import crud
from .dependencies import check_current_user
from .schemas import UserOut, UserBase
from application.backend.core.config import security

router = APIRouter(tags=["Users"])


@router.post("/register", response_model=UserOut, dependencies=[Depends(check_current_user(True))])
async def register_user(user_in: UserBase, session: AsyncSession = Depends(db_helper.session_dependency)):
    existing = await crud.get_user_by_username(session, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exist")
    return await crud.create_user(session, user_in)


@router.post("/login")
async def user_login(creds: UserBase, response: Response,
                     session: AsyncSession = Depends(db_helper.session_dependency)):
    user = await crud.authenticate_user(session, creds)
    if user:
        token = security.create_access_token(uid=str(user.username))
        security.set_access_cookies(token, response)
        return "ok"
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_current_user(True))])
async def user_delete(
        username: str,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    deleted = await crud.delete_user(session, username)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/logout")
async def logout(response: Response):
    security.unset_access_cookies(response)
    return "ok"
