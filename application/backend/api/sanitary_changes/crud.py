from fastapi import HTTPException, status
from sqlalchemy import select, exists
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import SanitaryChange, SanitaryTypeEnum, SanitaryBreak


async def get_sanitary_changes(session: AsyncSession, sanitary_type: SanitaryTypeEnum) -> list[SanitaryChange]:
    stmt = (
        select(SanitaryChange)
        .join(SanitaryChange.sanitary_break)
        .options(
            selectinload(SanitaryChange.user),
            selectinload(SanitaryChange.sanitary_break).selectinload(SanitaryBreak.object_from),
            selectinload(SanitaryChange.sanitary_break).selectinload(SanitaryBreak.object_to),

        )
        .where(SanitaryBreak.sanitary_type == sanitary_type)
        .order_by(SanitaryChange.id)
    )
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())