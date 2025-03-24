import uuid
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import Employee
from application.core import db_helper
from . import crud


async def employee_by_id(
        employee_id: Annotated[uuid.UUID, Path],
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> Employee:
    employee = await crud.get_employee(session=session, employee_id=employee_id)
    if employee is not None:
        return employee

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {employee_id} not found!",
    )
