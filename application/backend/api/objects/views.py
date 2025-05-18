from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from application.backend.api.users.dependencies import check_current_user
from application.backend.utils.notification_utils import create_notification
from . import crud
from .schemas import Object, ObjectCreate, ObjectUpdate

router = APIRouter(tags=["Object"])


@router.get("/", response_model=list[Object], dependencies=[Depends(check_current_user())])
async def get_objects(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_objects(session=session)


@router.post("/", response_model=Object, dependencies=[Depends(check_current_user(True))])
async def create_object(
        object_in: ObjectCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_object(session=session, object_in=object_in)


@router.post("/restore/{object_id}/", dependencies=[Depends(check_current_user(True))])
async def restore_object(
        object_id: int,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    object_restored = await crud.restore_object(session=session, object_id=object_id)
    background_tasks.add_task(
        create_notification,
        session=session,
        title="Восстановлен объект",
        message=f"Восстановлен объект: {object_restored.name}"
    )
    return None

@router.put("/{object_id}", response_model=Object, dependencies=[Depends(check_current_user(True))])
async def update_objects(
        object_id: int,
        object_in: ObjectUpdate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_object(session, object_in, object_id)


@router.delete("/{object_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_current_user(True))])
async def delete_object(
        object_id: int,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    object_deleted = await crud.delete_object(session=session, object_id=object_id)
    background_tasks.add_task(
        create_notification,
        session=session,
        title="Удалён объект",
        message=f"Удалён объект: {object_deleted.name}"
    )
    return None
