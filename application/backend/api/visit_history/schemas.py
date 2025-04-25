import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer

from application.backend.api.employees.schemas import Employee, EmployeeFullBase
from application.backend.api.objects.schemas import ObjectBase
from application.backend.core.models import VisitStatusEnum


class VisitHistoryBase(BaseModel):
    scanned_by_user_id: uuid.UUID
    employee_id: uuid.UUID
    status: VisitStatusEnum


class VisitHistoryCreate(VisitHistoryBase):
    pass


class VisitHistory(BaseModel):
    id: int
    entry_time: datetime
    exit_time: datetime | None
    object: ObjectBase
    employee: Employee
    scanned_by_user: Employee
    status: VisitStatusEnum
    model_config = ConfigDict(from_attributes=True)

    @field_serializer('entry_time')
    @field_serializer('exit_time')
    def serialize_time(self, dt: datetime, _info):
        return dt.strftime("%d-%m-%Y %H:%M:%S")

class VisitHistoryActive(BaseModel):
    id: int
    entry_time: datetime
    employee: Employee
    scanned_by_user: Employee
    status: VisitStatusEnum
    model_config = ConfigDict(from_attributes=True)

    @field_serializer('entry_time')
    def serialize_time(self, dt: datetime, _info):
        return dt.strftime("%d-%m-%Y %H:%M:%S")

class VisitHistoryActiveResponse(BaseModel):
    object: ObjectBase
    history: list[VisitHistoryActive]