import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import Employee, RoleEnum
from application.backend.core import db_helper
from application.backend.api.general_schemas.employee import EmployeeScanResult
from application.backend.api.visit_history.schemas import VisitHistoryLast
from application.backend.api.visit_history.dependencies import get_last_visit_by_id
from application.backend.api.sanitary_breaks.dependencies import get_sanitary_break

from . import crud


async def employee_by_id(
        employee_id: Annotated[uuid.UUID, Path],
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> Employee:
    employee = await crud.get_employee(session=session, employee_id=employee_id)
    if employee is not None:
        return employee

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee {employee_id} not found!",
    )

async def employee_search(
        session: AsyncSession,
        full_name: str | None = None,
        phone: str | None = None,
        group_id: int | None = None,
        object_id: int | None = None,
        offset: int = 0,
        count: int = 100
) -> list[Employee]:
    stmt = select(Employee).options(selectinload(Employee.group), selectinload(Employee.object))

    if full_name:
        stmt = stmt.where(Employee.full_name.ilike(f"%{full_name}%"))
    if phone:
        stmt = stmt.where(Employee.phone.ilike(f"%{phone}%"))

    if group_id is not None:
        if group_id == -1:
            stmt = stmt.where(Employee.group_id.is_(None))  # Ищем сотрудников без позиции
        else:
            stmt = stmt.where(Employee.group_id == group_id)

    if object_id is not None:
        if object_id == -1:
            stmt = stmt.where(Employee.object_id.is_(None))  # Ищем сотрудников без позиции
        else:
            stmt = stmt.where(Employee.object_id == object_id)

    stmt = stmt.offset(offset).limit(count).order_by(desc(Employee.id))
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_scan_employee_info(
        session: AsyncSession,
        employee: Employee,
        scanned_user: Employee
) -> EmployeeScanResult:
    last_visit = await get_last_visit_by_id(employee.id, session)

    last_visit_obj = None
    can_visit = True
    time_to_visit = None

    if last_visit:
        last_visit_obj = VisitHistoryLast.model_validate(last_visit, from_attributes=True)

        sanitary_break = await get_sanitary_break(
            last_visit.object_id,
            scanned_user.object_id,
            employee.sanitary_table,
            session
        )

        current_time_utc = datetime.now(tz=timezone.utc)

        if last_visit.exit_time and sanitary_break:
            can_visit = current_time_utc - last_visit.exit_time >= timedelta(hours=sanitary_break.time_break)
            time_to_visit = None if can_visit else (
                        last_visit.exit_time + timedelta(hours=sanitary_break.time_break)).astimezone()
        if last_visit.exit_time is None:
            can_visit = False

    return EmployeeScanResult(
        **employee.__dict__,
        last_visit=last_visit_obj,
        can_visit=can_visit,
        time_to_visit=time_to_visit
    )


async def get_scan_employee_info_by_id(employee_id: uuid.UUID, scanned_by_user_id: uuid.UUID, session: AsyncSession) -> EmployeeScanResult:
    employee: Employee | None = await session.get(Employee, employee_id)
    scanned_user: Employee | None = await session.get(Employee, scanned_by_user_id)
    if not scanned_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {scanned_by_user_id} not found!",
        )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found!",
        )

    return await get_scan_employee_info(session, employee, scanned_user)


async def get_security_by_id(
        employee_phone: str,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> Employee | None:
    stmt = select(Employee).options(
        selectinload(Employee.group),
        selectinload(Employee.object)
    ).where(Employee.phone == employee_phone, Employee.role == RoleEnum.security)
    result = await session.execute(stmt)
    employee: Employee = result.scalar_one_or_none()
    return employee


async def get_count_active_employees(session: AsyncSession) -> int:
    stmt = select(func.count()).where(Employee.is_deleted == False)
    result = await session.execute(stmt)
    count = result.scalar_one()
    return count