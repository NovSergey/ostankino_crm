from datetime import datetime
from enum import Enum
from urllib.parse import unquote

from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from application.backend.api.users.dependencies import check_current_user
from . import crud
from .dependencies import visit_history_search
from .schemas import VisitHistory, VisitHistoryCreate, VisitHistoryActiveResponse
from application.backend.api.objects.crud import get_object

router = APIRouter(tags=["Visit History"])

class VisitActionEnum(str, Enum):
    IN = 'in'
    OUT = 'out'


@router.get("/", response_model=list[VisitHistory], dependencies=[Depends(check_current_user())])
async def get_visit_history(
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_visit_history(session=session, offset=offset, count=count)


@router.post("/", response_model=VisitHistory, status_code=status.HTTP_201_CREATED)
async def create_visit_history(
        entry: VisitHistoryCreate,
        action: VisitActionEnum,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    if action == "in":
        return await crud.create_visit_history_in(session=session, entry=entry)
    else:
        return await crud.create_visit_history_out(session=session, entry=entry)


@router.get("/search", response_model=list[VisitHistory])
async def search_history(
        full_name: str = Query(""),
        object_id: int = Query(None),
        start_time: str = Query(None),  # Новый параметр для начальной даты
        end_time: str = Query(None),
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    try:
        start_time_dt = datetime.strptime(start_time, "%d-%m-%Y") if start_time else None
        end_time_dt = datetime.strptime(end_time, "%d-%m-%Y") if end_time else None
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format. Use DD-MM-YYYY (e.g., 26-04-2025).")
    return await visit_history_search(
        full_name=unquote(full_name),
        object_id=object_id,
        start_time=start_time_dt,
        end_time=end_time_dt,
        session=session,
        offset=offset,
        count=count
    )

@router.get("/active_users/{object_id}/", response_model=VisitHistoryActiveResponse)
async def get_active_users_in_object(
        object_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    object = await get_object(session, object_id)
    if not object:
        raise HTTPException(status_code=404, detail="Object not found")
    result = await crud.get_active_users(session=session, object_id=object_id)
    return {"object": object, "history": result}