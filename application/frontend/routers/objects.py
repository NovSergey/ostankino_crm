from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from application.frontend.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/")
async def get_objects_page(request: Request):
    return templates.TemplateResponse(name="objects.html", request=request)


@router.get("/{object_id}/")
async def get_object_page(object_id: int, request: Request):
    return templates.TemplateResponse("object.html", {"request": request, "object_id": object_id})
