import uuid
from datetime import datetime, time

from sqlalchemy import select, desc, Result, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import VisitHistory, Employee


async def visit_history_search(
        full_name: str | None,
        object_id: int | None,
        start_time: datetime | None,
        end_time: datetime | None,
        session: AsyncSession,
        offset: int = 0,
        count: int = 100
) -> list[VisitHistory]:
    stmt = select(VisitHistory).options(
        selectinload(VisitHistory.object),
        selectinload(VisitHistory.employee),
        selectinload(VisitHistory.scanned_by_user),
        selectinload(VisitHistory.employee).selectinload(Employee.object),
        selectinload(VisitHistory.employee).selectinload(Employee.group),
        selectinload(VisitHistory.scanned_by_user).selectinload(Employee.object),
        selectinload(VisitHistory.scanned_by_user).selectinload(Employee.group),
    ).join(VisitHistory.employee)
    if full_name:
        stmt = stmt.where(Employee.full_name.ilike(f"%{full_name}%"))
    if object_id is not None:
        if object_id == -1:
            stmt = stmt.where(VisitHistory.object_id.is_(None))
        else:
            stmt = stmt.where(VisitHistory.object_id == object_id)

    if start_time is not None:
        stmt = stmt.where(VisitHistory.entry_time >= start_time)
    if end_time is not None:
        end_time = datetime.combine(end_time.date(), time(23, 59, 59))
        stmt = stmt.where(VisitHistory.entry_time <= end_time)

    stmt = stmt.offset(offset).limit(count).order_by(desc(VisitHistory.entry_time))
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_last_visit_by_id(employee_id: uuid.UUID, session: AsyncSession) -> VisitHistory | None :
    stmt = (
        select(VisitHistory)
        .options(
            selectinload(VisitHistory.object),
            selectinload(VisitHistory.scanned_by_user),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.object),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.group),
        ).where(VisitHistory.employee_id == employee_id)
        .order_by(desc(VisitHistory.entry_time))
        .limit(1)
    )
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_count_visits(session: AsyncSession) -> int:
    now = datetime.now()
    start_of_day = datetime.combine(now.date(), time.min)
    end_of_day = datetime.combine(now.date(), time.max)
    print(start_of_day, end_of_day)
    stmt = select(func.count()).where(
        VisitHistory.entry_time >= start_of_day,
        VisitHistory.entry_time <= end_of_day
    )

    result = await session.execute(stmt)
    count = result.scalar_one()
    return count