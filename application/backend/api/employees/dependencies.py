import uuid
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.backend.core.models import Employee
from application.backend.core import db_helper
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

async def employee_search(full_name: str | None, position_id: int | None, session: AsyncSession) -> list[Employee]:
    stmt = select(Employee).options(selectinload(Employee.position))
    if full_name:
        stmt = stmt.where(Employee.full_name.ilike(f"%{full_name}%"))
    if position_id is not None:
        if position_id == -1:
            stmt = stmt.where(Employee.position_id.is_(None))  # Ищем сотрудников без позиции
        else:
            stmt = stmt.where(Employee.position_id == position_id)
    stmt = stmt.order_by(Employee.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())