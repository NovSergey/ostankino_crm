from fastapi import HTTPException
from sqlalchemy import select, desc, Result, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core.models import Notification


async def get_notifications(session: AsyncSession, active: bool, offset: int = 0, count: int = 100) -> list[Notification]:
    stmt = (
        select(Notification)
        .where(Notification.is_read == active)
        .offset(offset)
        .limit(count)
        .order_by(desc(Notification.time))
    )
    result: Result = await session.execute(stmt)
    notifications = result.scalars().all()
    return list(notifications)


async def read_notification(session: AsyncSession, notification_id: int):
    notification = await session.get(Notification, ident=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail=f"Not found notification {notification_id}")
    notification.is_read = True
    await session.commit()


async def read_all_notification(session: AsyncSession):
    stmt = (
        update(Notification)
        .where(Notification.is_read == False)
        .values(is_read=True)
    )
    await session.execute(stmt)
    await session.commit()