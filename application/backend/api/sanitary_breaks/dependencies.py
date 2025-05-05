from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from application.backend.core.models import SanitaryBreak, SanitaryTypeEnum


async def get_sanitary_break(object_from_id: int, object_to_id: int, table_type: SanitaryTypeEnum, session: AsyncSession) -> SanitaryBreak | None :
    stmt = (
        select(SanitaryBreak)
        .where(
            SanitaryBreak.object_from_id == object_from_id,
            SanitaryBreak.object_to_id == object_to_id,
            SanitaryBreak.sanitary_type == table_type
        )
        .limit(1)
    )
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()