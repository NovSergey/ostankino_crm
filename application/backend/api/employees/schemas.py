import uuid

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

from application.backend.api.general_schemas.base import CustomBaseModel
from application.backend.api.groups.schemas import Group
from application.backend.api.objects.schemas import Object
from application.backend.core.models import RoleEnum, SanitaryTypeEnum


class EmployeeBase(BaseModel):
    full_name: str
    phone: str
    role: RoleEnum
    group_id: int | None = None
    object_id: int | None = None
    sanitary_table: SanitaryTypeEnum

    @field_serializer("sanitary_table")
    def serialize_sanitary_table(self, sanitary: SanitaryTypeEnum, _info):
        return {
            "value": sanitary.value,
            "label": sanitary.label
        }

class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeCreate):
    full_name: str | None = None
    phone: str | None = None
    role: RoleEnum | None = None
    sanitary_table: SanitaryTypeEnum | None = None

class EmployeeFullBase(EmployeeBase):
    id: uuid.UUID

class Employee(CustomBaseModel):
    id: uuid.UUID
    full_name: str
    phone: str
    role: RoleEnum
    group: Group | None
    object: Object | None
    sanitary_table: SanitaryTypeEnum
    is_deleted: bool
    model_config = ConfigDict(from_attributes=True)

    @field_serializer("sanitary_table")
    def serialize_sanitary_table(self, sanitary: SanitaryTypeEnum, _info):
        return {
            "value": sanitary.value,
            "label": sanitary.label
        }