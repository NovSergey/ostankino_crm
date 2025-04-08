from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.api.visit_history.schemas import VisitHistoryCreate
from application.backend.core.models import VisitHistory, Employee


async def get_visit_history(session: AsyncSession, offset: int = 0, count: int = 100) -> list[VisitHistory]:
    stmt = (
        select(VisitHistory)
        .options(
            selectinload(VisitHistory.employee),
            selectinload(VisitHistory.object),
            selectinload(VisitHistory.scanned_by_user)
        )
        .offset(offset)
        .limit(count)
        .order_by(VisitHistory.entry_time)
    )
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def create_visit_history(session: AsyncSession, entry: VisitHistoryCreate) -> VisitHistory:
    entry_created = VisitHistory(**entry.model_dump())
    scanned_user = await session.get(Employee, entry_created.scanned_by_user_id)
    if not scanned_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {entry_created.scanned_by_user_id} not found!",
        )

    entry_created.object_id = scanned_user.object_id
    session.add(entry_created)
    await session.commit()
    result = await session.execute(
        select(VisitHistory)
        .options(
            selectinload(VisitHistory.object),
            selectinload(VisitHistory.employee),
            selectinload(VisitHistory.scanned_by_user),
        )
        .where(VisitHistory.id == entry_created.id)
    )
    return result.scalar_one()