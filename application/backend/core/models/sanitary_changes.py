from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .sanitary_breaks import SanitaryBreak
    from .users import User


class SanitaryChange(Base):
    __tablename__ = 'sanitary_changes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    sanitary_object_id: Mapped[int] = mapped_column(ForeignKey("sanitary_breaks.id"), nullable=False)
    sanitary_object: Mapped["SanitaryBreak"] = relationship()

    time_from: Mapped[int] = mapped_column(nullable=False)
    time_to: Mapped[int] = mapped_column(nullable=False)

    time_changed: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(foreign_keys=[user_id])