from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core.models import VisitHistory


async def get_visit_history(session: AsyncSession) -> list[VisitHistory]:
    stmt = select(VisitHistory).order_by(VisitHistory.entry_time)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())
