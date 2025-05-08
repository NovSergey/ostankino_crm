import asyncio
import io
import uuid
from urllib.parse import quote

import qrcode
from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

from application.backend.api.employees.dependencies import employee_by_id
from application.backend.api.employees.schemas import Employee
from application.backend.api.groups.crud import get_groups
from application.backend.api.objects.crud import get_objects
from application.backend.api.users.dependencies import jwt_required_redirect
from application.backend.core import db_helper
from application.backend.core.models import SanitaryTypeEnum
from application.frontend.config import settings

router = APIRouter(dependencies=[Depends(jwt_required_redirect())])
templates = Jinja2Templates(directory=settings.templates_folder)


@router.get("/")
async def get_employees_page(request: Request):
    return templates.TemplateResponse(name="employees.html", request=request)

@router.get("/add/")
async def get_employee_page(request: Request, session = Depends(db_helper.session_dependency)):
    objects = await get_objects(session)
    groups = await get_groups(session)
    return templates.TemplateResponse("employee_add.html", {
        "request": request,
        "groups": groups,
        "objects": objects,
        "sanitary_tables": SanitaryTypeEnum
    })

@router.get("/{employee_id}/")
async def get_employee_page(request: Request, session = Depends(db_helper.session_dependency), employee: Employee = Depends(employee_by_id)):
    employee = Employee.from_orm(employee)
    objects = await get_objects(session)
    groups = await get_groups(session)
    return templates.TemplateResponse("employee_detail.html", {
        "request": request,
        "employee": employee,
        "groups": groups,
        "objects": objects,
        "sanitary_tables": SanitaryTypeEnum
    })


@router.get("/employee/{employee_id}/qr", name="download_qr")
async def download_qr(employee: Employee = Depends(employee_by_id)):
    loop = asyncio.get_event_loop()
    buf = await loop.run_in_executor(None, generate_qr_image, employee.id)
    filename_utf8 = f"{employee.full_name}.png"
    filename_quoted = quote(filename_utf8)

    return StreamingResponse(buf, media_type="image/png", headers={
        "Content-Disposition": f"attachment; filename*=UTF-8''{filename_quoted}"
    })


def generate_qr_image(employee_id: uuid.UUID) -> io.BytesIO:
    img = qrcode.make(str(employee_id))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
