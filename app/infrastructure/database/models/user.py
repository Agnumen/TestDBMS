from typing import List, Optional
from sqlalchemy import (
    Enum as SqlEnum,
    text,
    BigInteger,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, not_null_str
from app.core.enums import UserRole

class User(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    language: Mapped[not_null_str]
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.USER,
        server_default=text("'USER'"),
    )
    is_alive: Mapped[bool] = mapped_column(
        default=True,
        server_default=text("'True'",),
    )
    banned: Mapped[bool] = mapped_column(
        default=False,
        server_default=text("'False'"),
    )
    
    activities: Mapped[List["Activity"]] = relationship(
        "Activity",
        back_populates="user",
        cascade="all, delete-orphan"
    )