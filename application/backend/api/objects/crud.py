from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from application.backend.core.models import Object

async def get_objects(session: AsyncSession) -> list[Object]:
    stmt = select(Object).order_by(Object.id)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())

async def get_object(session: AsyncSession, object_id: int) -> list[Object]:
    stmt = select(Object).order_by(Object.id)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())