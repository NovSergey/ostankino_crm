from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from application.backend.api.users.dependencies import check_current_user
from application.backend.api.users.schemas import UserOut
from application.frontend.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/")
async def get_settings_page(request: Request, user_jwt: UserOut = Depends(check_current_user())):
    return templates.TemplateResponse("settings.html", {"request": request, "user": user_jwt})