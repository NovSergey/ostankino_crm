from fastapi import APIRouter, status, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from application.backend.api.users.dependencies import check_current_user

from . import crud
from .schemas import NotificationBase

router = APIRouter(tags=["Notifications"], dependencies=[Depends(check_current_user())])


@router.get("/", response_model=list[NotificationBase])
async def get_notifications(
        active: bool,
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_notifications(session, active, offset, count)


@router.post("/read/{notification_id}")
async def get_notifications(
        notification_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.read_notification(session, notification_id)