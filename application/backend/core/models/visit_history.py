from typing import TYPE_CHECKING

import enum
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .objects import Object
    from .employees import Employee

class VisitStatusEnum(enum.Enum):
    success = "Успешно"
    error = "Ошибка"

class VisitHistory(Base):
    __tablename__ = 'visit_history'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    entry_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    exit_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id"), nullable=False)
    object: Mapped["Object"] = relationship(back_populates="visit_history")


    scanned_by_user_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    scanned_by_user: Mapped["Employee"] = relationship(foreign_keys=[scanned_by_user_id])

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee: Mapped["Employee"] = relationship(back_populates="visit_history", foreign_keys=[employee_id])

    status: Mapped[VisitStatusEnum] = mapped_column(PgEnum(VisitStatusEnum, name="visit_status_enum"), nullable=False)