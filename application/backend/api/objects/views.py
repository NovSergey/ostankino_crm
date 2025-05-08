from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from application.backend.api.users.dependencies import check_current_user
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

@router.put("/{object_id}", response_model=Object, dependencies=[Depends(check_current_user(True))])
async def update_objects(
        object_id: int,
        object_in: ObjectUpdate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_object(session, object_in, object_id)