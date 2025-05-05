from typing import TYPE_CHECKING

import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import RoleEnum, SanitaryTypeEnum

if TYPE_CHECKING:
    from .groups import Group
    from .objects import Object


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False) # сделать уникальным
    role: Mapped[RoleEnum] = mapped_column(PgEnum(RoleEnum, name="role_enum"), nullable=False)

    object_id: Mapped[int | None] = mapped_column(ForeignKey("objects.id"), nullable=True)
    object: Mapped["Object"] = relationship()

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)
    group: Mapped["Group"] = relationship()

    sanitary_table: Mapped[SanitaryTypeEnum] = mapped_column(PgEnum(SanitaryTypeEnum, name="sanitary_type_enum"),
                                                            nullable=False, server_default="main")

    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)