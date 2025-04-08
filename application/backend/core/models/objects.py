import enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from .base import Base

class ObjectStatusEnum(enum.Enum):
    open = "Открыт"
    close = "Закрыт"

class Object(Base):
    __tablename__ = 'objects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[ObjectStatusEnum] = mapped_column(PgEnum(ObjectStatusEnum, name="object_status_enum"), nullable=False)
