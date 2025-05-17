from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import SanitaryBreakBase
from application.backend.core.models import SanitaryBreak, SanitaryTypeEnum, SanitaryChange, Object


async def get_sanitary_breaks(session: AsyncSession, sanitary_type: SanitaryTypeEnum) -> list[SanitaryBreak]:
    stmt = select(SanitaryBreak).where(SanitaryBreak.sanitary_type == sanitary_type)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())

async def update_get_sanitary_breaks(
        session: AsyncSession,
        sanitary_break: SanitaryBreakBase,
        sanitary_type: SanitaryTypeEnum,
        user_id: int,
        time_changed: datetime
):
    stmt = select(SanitaryBreak).where(
        SanitaryBreak.sanitary_type == sanitary_type,
        SanitaryBreak.object_from_id == sanitary_break.object_from_id,
        SanitaryBreak.object_to_id == sanitary_break.object_to_id
    )
    result: Result = await session.execute(stmt)
    sanitary_update: SanitaryBreak = result.scalar_one_or_none()

    if not sanitary_update:
        object_from_exists = await session.execute(
            select(Object).where(Object.id == sanitary_break.object_from_id)
        )
        object_to_exists = await session.execute(
            select(Object).where(Object.id == sanitary_break.object_to_id)
        )

        if not object_from_exists.scalar_one_or_none() or not object_to_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both objects not found!"
            )

        sanitary_update = SanitaryBreak(
            sanitary_type=sanitary_type,
            object_from_id=sanitary_break.object_from_id,
            object_to_id=sanitary_break.object_to_id,
            time_break=sanitary_break.time_break,
        )

        old_time = 0
        session.add(sanitary_update)
        await session.commit()
    else:
        old_time = sanitary_update.time_break
        for name, value in sanitary_break.model_dump(exclude_unset=True).items():
            setattr(sanitary_update, name, value)
    await session.commit()

    sanitary_change = SanitaryChange(
        sanitary_break_id=sanitary_update.id,
        time_from=old_time,
        time_to=sanitary_update.time_break,
        user_id=user_id,
        time_changed=time_changed
    )

    session.add(sanitary_change)
    await session.commit()
