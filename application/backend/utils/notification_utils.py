from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core import db_helper
from application.backend.core.models import Notification, VisitHistory, Employee


async def create_notification(title: str, message: str, session: AsyncSession):
    entry_created = Notification(title=title, message=message)
    session.add(entry_created)
    await session.commit()

async def check_unfinished_visits_and_notify():
    async with db_helper.session_factory() as session:  # твой асинхронный session
        result: Result = await session.execute(
            select(VisitHistory)
            .options(
                selectinload(VisitHistory.employee),
                selectinload(VisitHistory.object),
                selectinload(VisitHistory.scanned_by_user),
            )
            .where(VisitHistory.exit_time.is_(None))
        )
        unfinished_visits: list[VisitHistory] = list(result.scalars().all())
        for unfinished_visit in unfinished_visits:
            await create_notification(
                title="Работник не вышел",
                message=f"Работник {unfinished_visit.employee.full_name} | {unfinished_visit.employee.phone} не вышел с объекта {unfinished_visit.object.name}",
                session=session
            )

