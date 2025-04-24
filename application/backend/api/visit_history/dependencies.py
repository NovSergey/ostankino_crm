from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import VisitHistory, Employee


async def visit_history_search(full_name: str | None, object_id: int | None, session: AsyncSession, offset: int = 0, count: int = 100) -> list[VisitHistory]:
    stmt = select(VisitHistory).options(
        selectinload(VisitHistory.object),
        selectinload(VisitHistory.employee),
        selectinload(VisitHistory.scanned_by_user),
        selectinload(VisitHistory.employee).selectinload(Employee.object),
        selectinload(VisitHistory.employee).selectinload(Employee.group),
        selectinload(VisitHistory.scanned_by_user).selectinload(Employee.object),
        selectinload(VisitHistory.scanned_by_user).selectinload(Employee.group),
    ).join(VisitHistory.employee)
    if full_name:
        stmt = stmt.where(Employee.full_name.ilike(f"%{full_name}%"))
    if object_id is not None:
        if object_id == -1:
            stmt = stmt.where(VisitHistory.object_id.is_(None))
        else:
            stmt = stmt.where(VisitHistory.object_id == object_id)
    stmt = stmt.offset(offset).limit(count).order_by(desc(VisitHistory.id))
    result = await session.execute(stmt)
    return list(result.scalars().all())