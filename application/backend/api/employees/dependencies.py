import uuid
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import select, desc
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

async def employee_search(
        full_name: str | None,
        phone: str | None,
        group_id: int | None,
        object_id: int | None,
        session: AsyncSession,
        offset: int = 0,
        count: int = 100
) -> list[Employee]:
    stmt = select(Employee).options(selectinload(Employee.group), selectinload(Employee.object))

    if full_name:
        stmt = stmt.where(Employee.full_name.ilike(f"%{full_name}%"))
    if phone:
        stmt = stmt.where(Employee.phone.ilike(f"%{phone}%"))

    if group_id is not None:
        if group_id == -1:
            stmt = stmt.where(Employee.group_id.is_(None))  # Ищем сотрудников без позиции
        else:
            stmt = stmt.where(Employee.group_id == group_id)

    if object_id is not None:
        if object_id == -1:
            stmt = stmt.where(Employee.object_id.is_(None))  # Ищем сотрудников без позиции
        else:
            stmt = stmt.where(Employee.object_id == object_id)

    stmt = stmt.offset(offset).limit(count).order_by(desc(Employee.id))
    result = await session.execute(stmt)
    return list(result.scalars().all())