from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core.models import Notification


async def get_count_active_notifications(session: AsyncSession) -> int:
    stmt = select(func.count()).where(Notification.is_read == False)
    result = await session.execute(stmt)
    count = result.scalar_one()
    return count