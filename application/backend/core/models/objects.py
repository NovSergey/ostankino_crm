from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .employees import Employee
    from .visit_history import VisitHistory

class Object(Base):
    __tablename__ = 'objects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    employees: Mapped[list["Employee"]] = relationship(back_populates="object")

    visit_history: Mapped[list["VisitHistory"]] = relationship(back_populates="object",
                                                               foreign_keys="[VisitHistory.object_id]")