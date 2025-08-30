from typing import Any, Awaitable, Callable, Dict, Optional
from aiogram import BaseMiddleware

from aiogram.types import TelegramObject
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

class DatabaseMiddleware(BaseMiddleware):
    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        isolation_level: Optional[str] = None,
        commit: bool = True
    ) -> None:
        self.session = session
        self.isolation_level = isolation_level
        self.commit = commit
        

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject, 
        data: Dict[str, Any]) -> Any:
        
        async with self.session() as session:
            try:
                data['session'] = session
                if self.isolation_level:
                    stmt = text("SET TRANSACTION ISOLATION LEVEL :level")
                    await session.execute(stmt, {"level": self.isolation_level})
                
                result = await handler(event, data)
                
                if self.commit:
                    await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e