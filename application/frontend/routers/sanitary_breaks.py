from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from application.frontend.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/employees")
async def get_sanitary_page(request: Request):
    return templates.TemplateResponse("sanitary_breaks.html", {"request": request, "type": "employees", 'name': "основные"})

@router.get("/tractor")
async def get_sanitary_page(request: Request):
    return templates.TemplateResponse("sanitary_breaks.html", {"request": request, "type": "tractor", 'name': "трактористов"})

@router.get("/car")
async def get_sanitary_page(request: Request):
    return templates.TemplateResponse("sanitary_breaks.html", {"request": request, "type": "car", 'name': "водителей"})
