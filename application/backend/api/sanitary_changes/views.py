from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.core import db_helper
from . import crud
from .schemas import SanitaryChangeBase
from application.backend.api.users.dependencies import check_current_user
from application.backend.core.models import SanitaryTypeEnum

router = APIRouter(tags=["Sanitary Changes"])



@router.get("/{sanitary_type}", response_model=list[SanitaryChangeBase], dependencies=[Depends(check_current_user())])
async def get_sanitary_breaks(
        sanitary_type: SanitaryTypeEnum,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_sanitary_changes(session=session, sanitary_type=sanitary_type)