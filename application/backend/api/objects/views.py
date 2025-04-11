from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from . import crud
from .schemas import Object
from application.backend.api.users.dependencies import check_current_user

router = APIRouter(tags=["Object"], dependencies=[Depends(check_current_user())])


@router.get("/", response_model=list[Object])
async def get_objects(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_objects(session=session)
