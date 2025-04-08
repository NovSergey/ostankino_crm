from typing import TYPE_CHECKING

import enum
import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .groups import Group
    from .objects import Object

class RoleEnum(enum.Enum):
    admin = "admin"
    employee = "employee"
    security = "security"

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[RoleEnum] = mapped_column(PgEnum(RoleEnum, name="role_enum"), nullable=False)

    object_id: Mapped[int | None] = mapped_column(ForeignKey("objects.id"), nullable=True)
    object: Mapped["Object"] = relationship()

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)
    group: Mapped["Group"] = relationship()