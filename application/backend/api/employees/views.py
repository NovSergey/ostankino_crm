import uuid
from urllib.parse import unquote

from fastapi import APIRouter, status, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from application.backend.api.general_schemas.employee import EmployeeScanResult
from application.backend.api.users.dependencies import check_current_user
from application.backend.utils.notification_utils import create_notification

from . import crud
from .dependencies import employee_by_id, employee_search, get_scan_employee_info, get_security_by_id
from .schemas import Employee, EmployeeCreate, EmployeeUpdate, EmployeePhone, EmployeeScanRequest

router = APIRouter(tags=["Employees"])


@router.get("/", response_model=list[Employee], dependencies=[Depends(check_current_user())])
async def get_employees(
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_employees(session, offset, count)


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(check_current_user())])
async def create_employee(
        employee_in: EmployeeCreate,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    check_employee = await employee_search(phone=employee_in.phone, session=session)
    if check_employee:
        raise HTTPException(
            status_code=409,
            detail=f"Employee with phone {employee_in.phone} already exists"
        )
    employee_new = await crud.create_employee(session=session, employee=employee_in)
    background_tasks.add_task(
        create_notification,
        session=session,
        title="Новый сотрудник",
        message=f"Добавлен сотрудник: {employee_new.full_name} | {employee_new.phone}"
    )
    return employee_new


@router.post("/get_security_by_phone/", response_model=Employee | None)
async def get_security_by_phone(
        employee_in: EmployeePhone,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await get_security_by_id(employee_in.phone, session)


@router.post("/scan_info/", response_model=EmployeeScanResult)
async def get_employee_scan_info(
        scan_info: EmployeeScanRequest,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    employee = await crud.get_employee(session, scan_info.employee_id)
    scanned_user = await crud.get_employee(session, scan_info.scanned_by_user_id)

    if employee is None or scanned_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {scan_info.employee_id} not found!",
        )

    return await get_scan_employee_info(session, employee, scanned_user)


@router.get("/search/", response_model=list[Employee], dependencies=[Depends(check_current_user())])
async def search_employees(
        full_name: str = Query(""),
        phone: str = Query(""),
        group_id: int = Query(None),
        object_id: int = Query(None),
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await employee_search(
        full_name=unquote(full_name),
        phone=unquote(phone),
        group_id=group_id,
        object_id=object_id,
        session=session,
        offset=offset,
        count=count
    )


@router.post("/restore/{employee_id}/", dependencies=[Depends(check_current_user())])
async def restore_employee(
        employee: Employee = Depends(employee_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.restore_employee(session=session, employee=employee)


@router.get("/{employee_id}/", response_model=Employee, dependencies=[Depends(check_current_user())])
async def get_employee(employee: Employee = Depends(employee_by_id)):
    return employee


@router.put("/{employee_id}/", response_model=Employee, dependencies=[Depends(check_current_user())])
async def update_employee(
        employee_update: EmployeeUpdate,
        employee: Employee = Depends(employee_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_employee(
        session=session,
        employee=employee,
        employee_update=employee_update,
    )


@router.delete("/{employee_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_current_user())])
async def delete_employee(
        background_tasks: BackgroundTasks,
        employee: Employee = Depends(employee_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    employee_deleted = await crud.delete_employee(session=session, employee=employee)
    background_tasks.add_task(
        create_notification,
        session=session,
        title="Удалён сотрудник",
        message=f"Удалён сотрудник: {employee.full_name} | {employee.phone}"
    )
    return employee_deleted