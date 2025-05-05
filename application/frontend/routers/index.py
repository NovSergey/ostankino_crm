from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from application.backend.api.users.dependencies import jwt_required_redirect
from application.frontend.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/", dependencies=[Depends(jwt_required_redirect())])
async def index(request: Request):
    return templates.TemplateResponse(name="base.html", request=request)


@router.get("/login/")
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", request=request)
