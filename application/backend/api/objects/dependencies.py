from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core.models import Object, ObjectStatusEnum


async def get_count_active_objects(session: AsyncSession) -> int:
    stmt = select(func.count()).where(Object.status == ObjectStatusEnum.open, Object.is_deleted == False)
    result = await session.execute(stmt)
    count = result.scalar_one()
    return count