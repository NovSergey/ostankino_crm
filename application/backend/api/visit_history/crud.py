import uuid
from datetime import datetime, timedelta
from typing import Tuple, Union

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


async def create_visit_history_in(session: AsyncSession, entry: VisitHistoryCreate) -> Union[VisitHistory, Tuple[None, str]] :
    entry_created = VisitHistory(**entry.model_dump())

    scanned_by_user, error = await get_valid_security(session, entry_created.scanned_by_user_id)
    if error:
        return None, error


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


async def create_visit_history_out(session: AsyncSession, entry: VisitHistoryCreate) -> Union[VisitHistory, Tuple[None, str]]:
    scanned_by_user, error = await get_valid_security(session, entry.scanned_by_user_id)
    if error:
        return None, error

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
            VisitHistory.employee_id == entry.employee_id
        )
        .order_by(desc(VisitHistory.entry_time))
        .limit(1)
    )
    visit_his = result.scalar_one_or_none()

    if not visit_his or visit_his.exit_time or visit_his.object_id != scanned_by_user.object_id:
        return None, "Не найдена история посещения"

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


async def get_valid_security(session: AsyncSession, user_id: uuid.UUID) -> Union[VisitHistory, Tuple[None, str]]:
    user = await session.get(Employee, user_id)
    if not user or user.role != RoleEnum.security:
        return None, f"Охранник {user_id} не найден!"
    if user.object_id is None:
        return None, f"Охранник {user_id} не назначен на объект!"
    return user, None