from pydantic import BaseModel, ConfigDict

class ObjectBase(BaseModel):
    name: str

class Object(ObjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)