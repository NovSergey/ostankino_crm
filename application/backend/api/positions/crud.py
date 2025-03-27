from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from application.backend.core.models import Position

async def get_positions(session: AsyncSession) -> list[Position]:
    stmt = select(Position).order_by(Position.id)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())
