from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import Employee, Group, Object, VisitHistory, SanitaryBreak
from application.backend.api.general_schemas.employee import EmployeeScanResult
from application.backend.api.visit_history.schemas import VisitHistoryLast

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


async def get_scan_employee_info(
        session: AsyncSession,
        employee: Employee,
        scanned_user: Employee
):
    stmt = (
        select(VisitHistory)
        .options(
            selectinload(VisitHistory.object),
            selectinload(VisitHistory.scanned_by_user),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.object),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.group),
        ).where(VisitHistory.employee_id == employee.id)
        .order_by(desc(VisitHistory.entry_time))
        .limit(1)
    )
    result: Result = await session.execute(stmt)
    last_visit: VisitHistory = result.scalar_one_or_none()

    last_visit_obj = None
    can_visit = True
    time_to_visit = None

    if last_visit:
        last_visit_obj = VisitHistoryLast.model_validate(last_visit, from_attributes=True)

        stmt = (
            select(SanitaryBreak)
            .where(
                SanitaryBreak.object_from_id == last_visit.object_id,
                SanitaryBreak.object_to_id == scanned_user.object_id,
            )
            .limit(1)
        )

        result: Result = await session.execute(stmt)
        sanitary_break = result.scalar_one_or_none()
        current_time_utc = datetime.now(tz=timezone.utc)

        if last_visit.exit_time and sanitary_break:
            can_visit = current_time_utc - last_visit.exit_time >= timedelta(hours=sanitary_break.time_break)
            time_to_visit = None if can_visit else (last_visit.exit_time + timedelta(hours=sanitary_break.time_break)).astimezone()
        if last_visit.exit_time is None:
            can_visit = False

    return EmployeeScanResult(
        **employee.__dict__,
        last_visit= last_visit_obj,
        can_visit=can_visit,
        time_to_visit=time_to_visit
    )


