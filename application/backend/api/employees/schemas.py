import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from application.backend.api.groups.schemas import Group
from application.backend.api.objects.schemas import Object
from application.backend.core.models import RoleEnum


class EmployeeBase(BaseModel):
    full_name: str
    phone: str
    role: RoleEnum
    group_id: int | None = None
    object_id: int | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeCreate):
    full_name: str | None = None
    phone: str | None = None
    role: RoleEnum | None = None

class Employee(BaseModel):
    id: uuid.UUID
    full_name: str
    phone: str
    role: RoleEnum
    group: Group | None
    object: Object | None
    model_config = ConfigDict(from_attributes=True)
