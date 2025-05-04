from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    full_name: str
    phone: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    phone: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class UserEdit(BaseModel):
    username: str | None = None
    full_name: str | None = None
    phone: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserChangePassword(BaseModel):
    username: str
    password: str
    new_password: str