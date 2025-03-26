from pydantic import BaseModel, ConfigDict

class PositionBase(BaseModel):
    title: str

class Position(PositionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)