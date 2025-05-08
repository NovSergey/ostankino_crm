from fastapi import APIRouter, Request, HTTPException
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.api.objects.crud import get_object
from application.backend.api.users.dependencies import jwt_required_redirect, check_current_user
from application.backend.api.users.schemas import UserOut
from application.backend.core import db_helper
from application.frontend.config import settings

router = APIRouter(dependencies=[Depends(jwt_required_redirect())])
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/")
async def get_objects_page(request: Request, user_jwt: UserOut = Depends(check_current_user())):
    return templates.TemplateResponse("objects.html", {"request":request, "user": user_jwt})

@router.get("/add/", dependencies=[Depends(check_current_user(True))])
async def add_object_page(request: Request):
    return templates.TemplateResponse("object_add.html", {"request": request})

@router.get("/edit/{object_id}", dependencies=[Depends(check_current_user(True))])
async def edit_object_page(
        object_id: int,
        request: Request,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    object = await get_object(session, object_id)
    return templates.TemplateResponse("object_detail.html", {"request": request, "object": object})

@router.get("/{object_id}/")
async def get_object_page(object_id: int, request: Request, user_jwt: UserOut = Depends(check_current_user())):
    return templates.TemplateResponse("object.html", {"request": request, "object_id": object_id, "user": user_jwt})

