import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer

from application.backend.api.employees.schemas import EmployeeFullBase
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
    scanned_by_user: EmployeeFullBase
    employee: EmployeeFullBase
    status: VisitStatusEnum
    model_config = ConfigDict(from_attributes=True)

class VisitHistoryActive(BaseModel):
    entry_time: datetime
    scanned_by_user: EmployeeFullBase
    employee: EmployeeFullBase
    model_config = ConfigDict(from_attributes=True)

    @field_serializer('entry_time')
    def serialize_time(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

class VisitHistoryActiveResponse(BaseModel):
    object: ObjectBase
    history: list[VisitHistoryActive]