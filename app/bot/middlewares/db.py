from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware

from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.infrastructure.database import Database

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker[AsyncSession]):
        self.session_pool = session_pool
        
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject, 
        data: Dict[str, Any]) -> Any:
        
        async with self.session_pool() as session:
            data['db'] = Database(session=session)
            try:
                result = await handler(event, data)
            
                await session.commit()
                
            except Exception as e:
                await session.rollback()
                raise e
            
            return result