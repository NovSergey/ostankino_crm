from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from application.backend.api.users.dependencies import jwt_required_redirect
from application.frontend.config import settings

router = APIRouter(dependencies=[Depends(jwt_required_redirect())])
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/")
async def get_visit_history_page(request: Request):
    return templates.TemplateResponse("visit_history.html", {"request": request})