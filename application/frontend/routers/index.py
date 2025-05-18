from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.api.employees.dependencies import get_count_active_employees
from application.backend.api.notifications.dependencies import get_count_active_notifications
from application.backend.api.objects.dependencies import get_count_active_objects
from application.backend.api.users.dependencies import jwt_required_redirect
from application.backend.api.visit_history.dependencies import get_count_visits
from application.backend.core import db_helper
from application.frontend.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/", dependencies=[Depends(jwt_required_redirect())])
async def index(request: Request, session: AsyncSession = Depends(db_helper.session_dependency)):
    employee_count = await get_count_active_employees(session)
    objects_count = await get_count_active_objects(session)
    visits_count = await get_count_visits(session)
    active_notifications_count = await get_count_active_notifications(session)
    return templates.TemplateResponse("index.html",
                                      {
                                          "request": request,
                                          "employee_count": employee_count,
                                          "objects_count": objects_count,
                                          "visits_count": visits_count,
                                          "notifications_count": active_notifications_count,
                                      })


@router.get("/login/")
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", request=request)
