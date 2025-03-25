from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models import Employee

from .schemas import EmployeeCreate, EmployeeUpdate


async def get_employees(session: AsyncSession) -> list[Employee]:
    stmt = select(Employee).order_by(Employee.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_employee(session: AsyncSession, employee_id: UUID) -> Employee | None:
    return await session.get(Employee, employee_id)


async def create_employee(session: AsyncSession, employee: EmployeeCreate) -> Employee:
    employee_created = Employee(**employee.model_dump())
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