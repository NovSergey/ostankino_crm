from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from . import crud
from .schemas import Position

router = APIRouter(tags=["Positions"])


@router.get("/", response_model=list[Position])
async def get_employees(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_positions(session=session)
