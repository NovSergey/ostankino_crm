import enum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SanitaryTypeEnum(enum.Enum):
    main = "main"
    car = "car"
    tractor = "tractor"

class SanitaryBreak(Base):
    __tablename__ = 'sanitary_breaks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    object_from_id: Mapped[int] = mapped_column(ForeignKey("objects.id"), nullable=False)
    # object_from: Mapped["Object"] = relationship(foreign_keys=[object_from_id])
    object_to_id: Mapped[int] = mapped_column(ForeignKey("objects.id"), nullable=False)
    # object_to: Mapped["Object"] = relationship(foreign_keys=[object_to_id])
    time_break: Mapped[int] = mapped_column(nullable=False)
    sanitary_type: Mapped[SanitaryTypeEnum] = mapped_column(PgEnum(SanitaryTypeEnum, name="sanitary_type_enum"),
                                                            nullable=False)