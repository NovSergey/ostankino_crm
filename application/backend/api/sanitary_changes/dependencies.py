from datetime import datetime, time

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import SanitaryChange, SanitaryBreak, SanitaryTypeEnum


async def sanitary_changes_search(
        sanitary_type: SanitaryTypeEnum,
        object_from_id: int | None,
        object_to_id: int | None,
        start_time: datetime | None,
        end_time: datetime | None,
        session: AsyncSession,
        offset: int = 0,
        count: int = 100
) -> list[SanitaryChange]:
    stmt = select(SanitaryChange).options(
        selectinload(SanitaryChange.user),
        selectinload(SanitaryChange.sanitary_break),
        selectinload(SanitaryChange.sanitary_break).selectinload(SanitaryBreak.object_from),
        selectinload(SanitaryChange.sanitary_break).selectinload(SanitaryBreak.object_to),

    ).join(SanitaryChange.sanitary_break).where(SanitaryBreak.sanitary_type == sanitary_type)

    if object_from_id is not None:
        stmt = stmt.where(SanitaryBreak.object_from_id == object_from_id)

    if object_to_id is not None:
        stmt = stmt.where(SanitaryBreak.object_to_id == object_to_id)

    if start_time is not None:
        stmt = stmt.where(SanitaryChange.time_changed >= start_time)
    if end_time is not None:
        end_time = datetime.combine(end_time.date(), time(23, 59, 59))
        stmt = stmt.where(SanitaryChange.time_changed <= end_time)

    stmt = stmt.offset(offset).limit(count).order_by(desc(SanitaryChange.time_changed))
    result = await session.execute(stmt)
    return list(result.scalars().all())