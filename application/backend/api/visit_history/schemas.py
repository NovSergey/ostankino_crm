import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from application.backend.api.employees.schemas import EmployeeBase
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
    scanned_by_user: EmployeeBase
    employee: EmployeeBase
    status: VisitStatusEnum
    model_config = ConfigDict(from_attributes=True)