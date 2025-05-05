
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import Employee, Group, Object, SanitaryTypeEnum

from .schemas import EmployeeCreate, EmployeeUpdate


async def get_employees(session: AsyncSession, offset: int = 0, count: int = 100) -> list[Employee]:
    stmt = (
        select(Employee)
        .options(
            selectinload(Employee.group),
            selectinload(Employee.object)
        )
        .where(Employee.is_deleted == False)
        .offset(offset)
        .limit(count)
        .order_by(desc(Employee.id))
    )
    result: Result = await session.execute(stmt)
    employees = result.scalars().all()
    return list(employees)


async def get_employee(session: AsyncSession, employee_id: UUID) -> Employee | None:
    stmt = select(Employee).options(selectinload(Employee.group), selectinload(Employee.object)).where(
        Employee.id == employee_id)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_employee(session: AsyncSession, employee: EmployeeCreate) -> Employee:
    employee_created = Employee(**employee.model_dump())
    if employee.sanitary_table:
        employee_created.sanitary_table = employee.sanitary_table.value
    if employee.group_id:
        employee_created.group = await session.get(Group, employee.group_id)
    if employee.object_id:
        employee_created.object = await session.get(Object, employee.object_id)
    if (employee.group_id is not None and employee_created.group is None) or (
            employee.object_id is not None and employee_created.object is None):
        raise HTTPException(status_code=404, detail="Incorrect data")
    session.add(employee_created)
    await session.commit()
    return employee_created


async def update_employee(
        session: AsyncSession,
        employee: Employee,
        employee_update: EmployeeUpdate
) -> Employee:
    for name, value in employee_update.model_dump(exclude_unset=True).items():
        if name == "sanitary_table" and isinstance(value, dict):
            value = SanitaryTypeEnum(value["value"])
        setattr(employee, name, value)
    await session.commit()
    return employee


async def delete_employee(
        session: AsyncSession,
        employee: Employee,
) -> None:
    employee.is_deleted = True
    await session.commit()


async def restore_employee(
        session: AsyncSession,
        employee: Employee,
) -> None:
    employee.is_deleted = False
    await session.commit()