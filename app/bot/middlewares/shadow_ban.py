import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, User
from app.infrastructure.database import Database
# get_user_banned_status_by_id

logger = logging.getLogger(__name__)


class ShadowBanMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)
        
        db: Database = data.get("db")
        if db is None:
            logger.error("Database connection not found in middleware data.")
            raise RuntimeError("Missing database connection for shadow ban check.")
        
        user_banned_status = await db.user.get_user_banned_status_by_id(user_id=user.id)

        if user_banned_status:
            logger.warning("Shadow-banned user tried to interact: %d", user.id)
            if event.callback_query:
                await event.callback_query.answer()
            return 

        return await handler(event, data)