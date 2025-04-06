from pydantic import BaseModel, ConfigDict

class GroupBase(BaseModel):
    title: str

class Group(GroupBase):
    id: int
    model_config = ConfigDict(from_attributes=True)