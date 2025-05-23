from fastapi import APIRouter, HTTPException, Response, Depends, status, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from application.backend.core.models import User
from . import crud
from .dependencies import check_current_user
from .schemas import UserOut, UserBase, UserLogin, UserEdit, UserChangePassword
from application.backend.core.config import security
from ...utils.limiter import limiter

router = APIRouter(tags=["Users"])

@router.get("/", response_model=list[UserOut], dependencies=[Depends(check_current_user(True))])
async def get_users(
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_users(session, offset, count)

@router.post("/register/", response_model=UserOut, dependencies=[Depends(check_current_user(True))])
async def register_user(user_in: UserBase, session: AsyncSession = Depends(db_helper.session_dependency)):
    existing = await crud.get_user_by_username(session, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exist")
    return await crud.create_user(session, user_in)


@router.post("/login/")
@limiter.limit("5/10minute")
async def user_login(request: Request, creds: UserLogin, response: Response,
                     session: AsyncSession = Depends(db_helper.session_dependency)):
    user = await crud.authenticate_user(session, creds)
    if user:
        token = security.create_access_token(uid=str(user.username))
        security.set_access_cookies(token, response)
        return "ok"

    raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.put("/{username}/")
async def user_update(
        username: str,
        change_info: UserEdit,
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_jwt: User = Depends(check_current_user()),
):
    if not (user_jwt.username == username or user_jwt.is_superuser):
        raise HTTPException(status_code=403, detail="Access denied")

    user = await crud.edit_user(session, username, change_info)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"result": "ok"}


@router.delete("/{username}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_current_user(True))])
async def user_delete(
        username: str,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    deleted = await crud.delete_user(session, username)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/change_password/")
async def change_password(
        creds: UserChangePassword,
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_jwt: User = Depends(check_current_user())
):
    if user_jwt.username != creds.username:
        raise HTTPException(status_code=403, detail="Access denied")
    user = await crud.change_password_user(session, creds)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"result": "ok"}


@router.get("/logout/")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    security.unset_access_cookies(response)
    return response