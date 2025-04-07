import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from application.backend.core.models import VisitStatusEnum


class VisitHistoryBase(BaseModel):
    object_id: int
    scanned_by_user_id: uuid.UUID
    employee_id: uuid.UUID
    status: VisitStatusEnum

class VisitHistory(BaseModel):
    id: int
    entry_time: datetime
    exit_time: datetime | None
    object_id: int
    scanned_by_user_id: uuid.UUID
    employee_id: uuid.UUID
    status: VisitStatusEnum
    model_config = ConfigDict(from_attributes=True)