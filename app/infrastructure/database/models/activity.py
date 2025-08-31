from datetime import date
from sqlalchemy import (
    text,
    BigInteger,
    Integer,
    ForeignKey,
    func,
    Date,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.infrastructure.database.models import Base, User
from .base import Base

class Activity(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    
    activity_date: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date(),
        onupdate=func.current_date(),
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

    __table_args__ = (
        UniqueConstraint("user_id", "activity_date", name="idx_activity_user_day"),
    )