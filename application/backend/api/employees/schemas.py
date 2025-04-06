import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from application.backend.api.groups.schemas import Position


class EmployeeBase(BaseModel):
    full_name: str
    position_id: int | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeCreate):
    full_name: str | None = None


class Employee(BaseModel):
    id: uuid.UUID
    full_name: str
    position: Position | None
    model_config = ConfigDict(from_attributes=True)
