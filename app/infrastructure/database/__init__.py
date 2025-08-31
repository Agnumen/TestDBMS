from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.infrastructure.database.models import Base
from app.infrastructure.database.repositories import UserRepository, ActivityRepository

class Database:
    def __init__(self, session: AsyncSession):
        self.user = UserRepository(session=session)
        self.activity = ActivityRepository(session=session)
        

async def create_tables(engine: AsyncEngine):
    """Создает все таблицы в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables(engine: AsyncEngine):
    """Удаляет все таблицы из базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)