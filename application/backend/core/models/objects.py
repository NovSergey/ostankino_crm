from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from .base import Base
from .enums import ObjectStatusEnum


class Object(Base):
    __tablename__ = 'objects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[ObjectStatusEnum] = mapped_column(PgEnum(ObjectStatusEnum, name="object_status_enum"), nullable=False)
