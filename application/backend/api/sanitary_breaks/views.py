from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from . import crud
from .schemas import SanitaryBreakBase
from application.backend.api.users.dependencies import check_current_user
from application.backend.core.models import SanitaryTypeEnum, User
from application.backend.utils.notification_utils import create_notification

router = APIRouter(tags=["Sanitary Breaks"])



@router.get("/{sanitary_type}", response_model=list[SanitaryBreakBase], dependencies=[Depends(check_current_user())])
async def get_sanitary_breaks(
        sanitary_type: SanitaryTypeEnum,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_sanitary_breaks(session=session, sanitary_type=sanitary_type)

@router.put("/{sanitary_type}")
async def update_sanitary_breaks(
        sanitary_type: SanitaryTypeEnum,
        sanitary_breaks: list[SanitaryBreakBase],
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_jwt: User = Depends(check_current_user())
):
    for sanitary_break in sanitary_breaks:
        if sanitary_break.object_to_id == sanitary_break.object_from_id:
            raise HTTPException(status_code=404, detail="Cannot save object_from_id equal to object_to_id")
    for sanitary_break in sanitary_breaks:
        await crud.update_get_sanitary_breaks(session=session, sanitary_break=sanitary_break, sanitary_type=sanitary_type, user_id=user_jwt.id)

    type_to_string = {
        sanitary_type.main: "основных работников",
        sanitary_type.car: "водителей",
        sanitary_type.tractor: "трактористов"
    }

    background_tasks.add_task(
        create_notification,
        session=session,
        title="Изменение санитарных разрывов",
        message=f"Внесены изменения в таблицу санитарных разрывов для {type_to_string[sanitary_type]}"
    )
    return "ok"
