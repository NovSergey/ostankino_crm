import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer

from application.backend.api.employees.schemas import Employee
from application.backend.api.general_schemas.base import CustomBaseModel
from application.backend.api.objects.schemas import ObjectBase
from application.backend.core.models import VisitStatusEnum


class VisitHistoryBase(BaseModel):
    scanned_by_user_id: uuid.UUID
    employee_id: uuid.UUID
    status: VisitStatusEnum


class VisitHistoryCreate(VisitHistoryBase):
    pass


class VisitHistory(CustomBaseModel):
    id: int
    entry_time: datetime
    exit_time: datetime | None
    object: ObjectBase
    employee: Employee
    scanned_by_user: Employee
    status: VisitStatusEnum
    model_config = ConfigDict(from_attributes=True)


class VisitHistoryActive(CustomBaseModel):
    id: int
    entry_time: datetime
    employee: Employee
    scanned_by_user: Employee
    status: VisitStatusEnum
    model_config = ConfigDict(from_attributes=True)

class VisitHistoryActiveResponse(BaseModel):
    object: ObjectBase
    history: list[VisitHistoryActive]

class VisitHistoryLast(CustomBaseModel):
    id: int
    entry_time: datetime
    exit_time: datetime | None
    object: ObjectBase
    scanned_by_user: Employee