from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy import select, desc, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.api.visit_history.schemas import VisitHistoryCreate
from application.backend.core.models import VisitHistory, Employee, RoleEnum


async def get_visit_history(session: AsyncSession, offset: int = 0, count: int = 100) -> list[VisitHistory]:
    stmt = (
        select(VisitHistory)
        .options(
            selectinload(VisitHistory.employee),
            selectinload(VisitHistory.object),
            selectinload(VisitHistory.scanned_by_user),
            selectinload(VisitHistory.employee).selectinload(Employee.object),
            selectinload(VisitHistory.employee).selectinload(Employee.group),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.object),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.group),
        )
        .offset(offset)
        .limit(count)
        .order_by(desc(VisitHistory.entry_time))
    )
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def create_visit_history_in(session: AsyncSession, entry: VisitHistoryCreate) -> VisitHistory:
    entry_created = VisitHistory(**entry.model_dump())
    scanned_by_user = await session.get(Employee, entry_created.scanned_by_user_id)
    if not scanned_by_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {entry_created.scanned_by_user_id} not found!",
        )

    if scanned_by_user.object_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security {entry.scanned_by_user_id} is not assigned to the object!",
        )

    entry_created.object_id = scanned_by_user.object_id
    session.add(entry_created)
    await session.commit()

    result = await session.execute(
        select(VisitHistory)
        .options(
            selectinload(VisitHistory.employee),
            selectinload(VisitHistory.object),
            selectinload(VisitHistory.scanned_by_user),
            selectinload(VisitHistory.employee).selectinload(Employee.object),
            selectinload(VisitHistory.employee).selectinload(Employee.group),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.object),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.group),
        )
        .where(VisitHistory.id == entry_created.id)
    )
    return result.scalar_one()


async def create_visit_history_out(session: AsyncSession, entry: VisitHistoryCreate) -> VisitHistory:
    scanned_by_user = await session.get(Employee, entry.scanned_by_user_id)
    if not scanned_by_user or scanned_by_user.role != RoleEnum.security:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security {entry.scanned_by_user_id} not found!",
        )
    if scanned_by_user.object_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security {entry.scanned_by_user_id} is not assigned to the object!",
        )
    result = await session.execute(
        select(VisitHistory)
        .options(
            selectinload(VisitHistory.employee),
            selectinload(VisitHistory.object),
            selectinload(VisitHistory.scanned_by_user),
            selectinload(VisitHistory.employee).selectinload(Employee.object),
            selectinload(VisitHistory.employee).selectinload(Employee.group),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.object),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.group),
        )
        .where(
            VisitHistory.employee_id == entry.employee_id,
            VisitHistory.object_id == scanned_by_user.object_id,
            VisitHistory.exit_time == None,
        )
        .order_by(desc(VisitHistory.entry_time))
        .limit(1)
    )
    visit_his = result.scalar_one_or_none()
    if not visit_his:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found visit history",
        )
    visit_his.exit_time = datetime.now()
    await session.commit()
    return visit_his


async def get_active_users(session: AsyncSession, object_id: int) -> list[VisitHistory]:
    two_days_ago = datetime.utcnow() - timedelta(days=1)
    subquery = (
        select(
            func.max(VisitHistory.entry_time).label("latest_entry"),
            VisitHistory.employee_id
        )
        .where(
            VisitHistory.object_id == object_id,
            VisitHistory.exit_time == None,
            VisitHistory.entry_time >= two_days_ago
        )
        .group_by(VisitHistory.employee_id)
        .subquery()
    )

    stmt = (
        select(VisitHistory)
        .join(
            subquery,
            (VisitHistory.employee_id == subquery.c.employee_id) &
            (VisitHistory.entry_time == subquery.c.latest_entry)
        )
        .options(
            selectinload(VisitHistory.employee),
            selectinload(VisitHistory.employee).selectinload(Employee.object),
            selectinload(VisitHistory.employee).selectinload(Employee.group),
            selectinload(VisitHistory.scanned_by_user),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.object),
            selectinload(VisitHistory.scanned_by_user).selectinload(Employee.group),
        )
    )
    result = await session.execute(stmt)

    return list(result.scalars().all())