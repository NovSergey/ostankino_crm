from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from application.backend.api.users.dependencies import jwt_required_redirect
from application.frontend.config import settings

router = APIRouter(dependencies=[Depends(jwt_required_redirect())])
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/main/")
async def get_sanitary_page(request: Request):
    return templates.TemplateResponse("sanitary_breaks.html", {"request": request, "type": "main", 'name': "основные"})

@router.get("/tractor/")
async def get_sanitary_page(request: Request):
    return templates.TemplateResponse("sanitary_breaks.html", {"request": request, "type": "tractor", 'name': "трактористов"})

@router.get("/car/")
async def get_sanitary_page(request: Request):
    return templates.TemplateResponse("sanitary_breaks.html", {"request": request, "type": "car", 'name': "водителей"})
