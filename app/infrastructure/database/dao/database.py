from typing import Annotated
from datetime import datetime

from config import settings

from sqlalchemy import func, TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = settings.get_db_url()
engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

uniq_str_an = Annotated[str, mapped_column(unique=True)]
uniq_int_an = Annotated[int, mapped_column(unique=True, nullable=False)]
not_null_str = Annotated[str, mapped_column(nullable=False)]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True # Базовый класс будет абстрактным, чтобы не создавать отдельную таблицу для него
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
    )
    
    
    # @classmethod
    # @property
    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__.lower()
        return name[:-1] + "ies" if name[-1] == "y" else name + "s"
    

async def create_tables_sqlite():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        