from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from . import crud
from .schemas import Group
from ..users.dependencies import check_current_user

router = APIRouter(tags=["Groups"], dependencies=[Depends(check_current_user())])


@router.get("/", response_model=list[Group])
async def get_groups(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_groups(session=session)
