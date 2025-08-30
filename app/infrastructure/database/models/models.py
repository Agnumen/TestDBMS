from typing import List
from datetime import datetime
from sqlalchemy import (
    Enum as SqlEnum,
    text,
    Integer,
    BigInteger,
    ForeignKey,
    func,
    TIMESTAMP
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.dao.database import Base, not_null_str
from app.infrastructure.database.enums.roles import UserRole

class User(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[not_null_str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    language: Mapped[not_null_str]
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.USER,
        server_default=text("'USER'"),
        # nullable=False
    )
    is_alive: Mapped[bool] = mapped_column(
        default=True,
        server_default=text("'True'",),
        # nullable=False
    )
    banned: Mapped[bool] = mapped_column(
        default=False,
        server_default=text("'False'"),
        # nullable=False,
    )
    
    activities: Mapped[List["Activity"]] = relationship(
        "Activity",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
class Activity(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    activity_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        # nullable=False,
    )
    
    actions: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default=text("'1'"),
        nullable=False,
    )
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates="activities",
    )