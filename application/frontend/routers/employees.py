import uuid

from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.templating import Jinja2Templates

from application.backend.api.employees.dependencies import employee_by_id
from application.backend.api.employees.schemas import Employee, EmployeeBase
from application.backend.api.groups.crud import get_groups
from application.backend.api.objects.crud import get_objects
from application.backend.api.users.dependencies import jwt_required_redirect
from application.backend.core import db_helper
from application.frontend.config import settings

router = APIRouter(dependencies=[Depends(jwt_required_redirect())])
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/")
async def get_employees_page(request: Request):
    return templates.TemplateResponse(name="employees.html", request=request)

@router.get("/add")
async def get_employee_page(request: Request, session = Depends(db_helper.session_dependency)):
    objects = await get_objects(session)
    groups = await get_groups(session)
    return templates.TemplateResponse("employee_add.html", {
        "request": request,
        "groups": groups,
        "objects": objects
    })

@router.get("/{employee_id}")
async def get_employee_page(request: Request, session = Depends(db_helper.session_dependency), employee: Employee = Depends(employee_by_id)):
    employee = Employee.from_orm(employee)
    objects = await get_objects(session)
    groups = await get_groups(session)
    return templates.TemplateResponse("employee_detail.html", {
        "request": request,
        "employee": employee,
        "groups": groups,
        "objects": objects
    })



