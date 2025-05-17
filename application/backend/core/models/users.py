from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default="true", nullable=False)
    is_superuser: Mapped[bool] = mapped_column(server_default="false", nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)