import uuid

from pydantic import BaseModel, ConfigDict

class EmployeeBase(BaseModel):
    full_name: str
    position: str


class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeCreate):
    full_name: str | None = None
    position: str | None = None


class Employee(EmployeeBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
