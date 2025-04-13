from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from application.backend.api.users.dependencies import check_current_user
from . import crud
from .schemas import VisitHistory, VisitHistoryCreate, VisitHistoryActiveResponse
from application.backend.api.objects.crud import get_object

router = APIRouter(tags=["Visit History"])


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
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_visit_history(session=session, entry=entry)

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