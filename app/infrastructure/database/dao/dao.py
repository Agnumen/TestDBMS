from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.database.dao.base import BaseDAO
from app.infrastructure.database.models.models import User, Activity

class UserDAO(BaseDAO):
    model = User
    
    @classmethod
    async def change_user_alive_status(cls, session: AsyncSession, is_alive: bool, user_id: int):
        stmt = (
            update(cls.model)
            .filter_by(user_id=user_id)
            .values(is_alive=is_alive)
        )
        try:
            await session.execute(stmt)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    @classmethod
    async def get_user_lang(cls, session: AsyncSession, user_id: int):
        stmt = (
            select(cls.model.language)
            .filter_by(user_id=user_id)
        )
        try:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e

class ActivityDAO(BaseDAO):
    model = Activity