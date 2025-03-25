from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core import db_helper
from . import crud
from .dependencies import employee_by_id
from .schemas import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter(tags=["Employees"])


@router.get("/", response_model=list[Employee])
async def get_employees(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_employees(session=session)


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(
        employee_in: EmployeeCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_employee(session=session, employee=employee_in)


@router.get("/{employee_id}/", response_model=Employee)
async def get_employee(employee: Employee = Depends(employee_by_id)):
    return employee


@router.put("/{employee_id}/")
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
