from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from . import crud
from .schemas import VisitHistory

router = APIRouter(tags=["Visit History"])


@router.get("/", response_model=list[VisitHistory])
async def get_visit_history(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_visit_history(session=session)
