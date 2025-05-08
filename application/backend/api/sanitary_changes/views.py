from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from . import crud
from .dependencies import sanitary_changes_search
from .schemas import SanitaryChangeBase
from application.backend.api.users.dependencies import check_current_user
from application.backend.core.models import SanitaryTypeEnum

router = APIRouter(tags=["Sanitary Changes"], dependencies=[Depends(check_current_user())])



@router.get("/{sanitary_type}/", response_model=list[SanitaryChangeBase])
async def get_sanitary_breaks(
        sanitary_type: SanitaryTypeEnum,
        offset: int = Query(0, ge=0),
        count: int = Query(100, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency),
):    return await crud.get_sanitary_changes(session=session, sanitary_type=sanitary_type, offset=offset, count=count)


@router.get("/search/{sanitary_type}/", response_model=list[SanitaryChangeBase])
async def search_changes(
        sanitary_type: SanitaryTypeEnum,
        object_from_id: int = Query(None),
        object_to_id: int = Query(None),
        start_time: str = Query(None),
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
    return await sanitary_changes_search(
        sanitary_type=sanitary_type,
        object_from_id=object_from_id,
        object_to_id=object_to_id,
        start_time=start_time_dt,
        end_time=end_time_dt,
        session=session,
        offset=offset,
        count=count
    )