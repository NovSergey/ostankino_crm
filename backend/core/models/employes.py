from typing import TYPE_CHECKING

import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .positions import Position

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=True)
    position: Mapped["Position"] = relationship(back_populates="employees")