from urllib.parse import unquote

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from . import crud
from .dependencies import employee_by_id, employee_search
from .schemas import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter(tags=["Employees"])


@router.get("/", response_model=list[Employee])
async def get_employees(
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_employees(session, offset, count)


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(
        employee_in: EmployeeCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_employee(session=session, employee=employee_in)


@router.get("/{employee_id}/", response_model=Employee)
async def get_employee(employee: Employee = Depends(employee_by_id)):
    return employee


@router.get("/search", response_model=list[Employee])
async def search_employees(
        full_name: str = Query(""),
        group_id: int = Query(None),
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await employee_search(
        full_name=unquote(full_name),
        group_id=group_id,
        session=session,
        offset=offset,
        count=count
    )


@router.put("/{employee_id}/", response_model=Employee)
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


@router.delete("/{employee_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
        employee: Employee = Depends(employee_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_employee(session=session, employee=employee)
