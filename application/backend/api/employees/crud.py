from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import Employee, Group, Object

from .schemas import EmployeeCreate, EmployeeUpdate


async def get_employees(session: AsyncSession) -> list[Employee]:
    stmt = select(Employee).options(selectinload(Employee.group), selectinload(Employee.object)).order_by(Employee.id)
    #stmt = select(Employee).order_by(Employee.id)
    result: Result = await session.execute(stmt)
    employees = result.scalars().all()
    return list(employees)


async def get_employee(session: AsyncSession, employee_id: UUID) -> Employee | None:
    stmt = select(Employee).options(selectinload(Employee.group), selectinload(Employee.object)).where(Employee.id == employee_id)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_employee(session: AsyncSession, employee: EmployeeCreate) -> Employee:
    employee_created = Employee(**employee.model_dump())
    if employee.group_id:
        employee_created.group = await session.get(Group, employee.group_id)
    if employee.object_id:
        employee_created.object = await session.get(Object, employee.object_id)
    session.add(employee_created)
    await session.commit()
    return employee_created


async def update_employee(
    session: AsyncSession,
    employee: Employee,
    employee_update: EmployeeUpdate
) -> Employee:
    for name, value in employee_update.model_dump(exclude_unset=True).items():
        setattr(employee, name, value)
    await session.commit()
    return employee


async def delete_employee(
    session: AsyncSession,
    employee: Employee,
) -> None:
    await session.delete(employee)
    await session.commit()

