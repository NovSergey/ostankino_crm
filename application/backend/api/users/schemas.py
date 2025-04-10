from pydantic import BaseModel, ConfigDict


from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str
