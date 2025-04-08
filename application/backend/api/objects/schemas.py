from pydantic import BaseModel, ConfigDict

from application.backend.core.models import ObjectStatusEnum


class ObjectBase(BaseModel):
    name: str
    status: ObjectStatusEnum

class Object(ObjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)