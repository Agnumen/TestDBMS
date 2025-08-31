from typing import Annotated
from datetime import datetime

from sqlalchemy import func, TIMESTAMP, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs


uniq_str_an = Annotated[str, mapped_column(unique=True)]
uniq_int_an = Annotated[int, mapped_column(unique=True, nullable=False)]
not_null_str = Annotated[str, mapped_column(String, nullable=False)]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True # Базовый класс будет абстрактным, чтобы не создавать отдельную таблицу для него
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
    )
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__.lower()
        if name.endswith("y"):
            return name[:-1] + "ies"
        elif name.endswith(("s", "x", "ch", "sh")):
            return name[:-1] + "es"
        else:
            return name + "s"
    

