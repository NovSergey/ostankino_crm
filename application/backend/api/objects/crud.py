from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from application.backend.api.objects.schemas import ObjectCreate, ObjectUpdate
from application.backend.core.models import Object


async def get_objects(session: AsyncSession) -> list[Object]:
    stmt = select(Object).where(Object.is_deleted == False).order_by(Object.id)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_object(session: AsyncSession, object_id: int) -> Object:
    stmt = select(Object).where(Object.id == object_id)
    result: Result = await session.execute(stmt)
    current_object = result.scalar_one_or_none()
    if not current_object:
        raise HTTPException(status_code=404, detail="Object not found")
    return current_object


async def create_object(session: AsyncSession, object_in: ObjectCreate) -> Object:
    check_object = await session.execute(select(Object).where(Object.name == object_in.name))
    if check_object.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Object already exist")
    object_created = Object(**object_in.model_dump())
    session.add(object_created)
    await session.commit()
    return object_created


async def update_object(session: AsyncSession, object_in: ObjectUpdate, object_id: int) -> Object:
    old_object = await get_object(session, object_id)

    for name, value in object_in.model_dump(exclude_unset=True).items():
        setattr(old_object, name, value)

    await session.commit()
    return old_object


async def delete_object(session: AsyncSession, object_id: int) -> Object:
    current_object = await get_object(session, object_id)
    current_object.is_deleted = True
    await session.commit()
    return current_object


async def restore_object(session: AsyncSession, object_id: int) -> Object:
    current_object = await get_object(session, object_id)
    current_object.is_deleted = False
    await session.commit()
    return current_object