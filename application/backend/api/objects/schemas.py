from pydantic import BaseModel, ConfigDict

from application.backend.core.models import ObjectStatusEnum


class ObjectBase(BaseModel):
    name: str
    status: ObjectStatusEnum
    is_deleted: bool
    model_config = ConfigDict(from_attributes=True)


class ObjectCreate(BaseModel):
    name: str


class ObjectUpdate(BaseModel):
    name: str | None = None
    status: ObjectStatusEnum | None = None


class Object(ObjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
