import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache


logger = logging.getLogger(__name__)

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
        self,
        throttle_message_time: int=1,
        throttle_callback_time: int=1,
    ):
        self.message_cache = TTLCache(maxsize=10_000, ttl=throttle_message_time)
        self.callback_cache = TTLCache(maxsize=10_000, ttl=throttle_callback_time)
        
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        # logger.debug(
        #     'Вошли в миддлварь %s, тип события %s',
        #     __class__.__name__,
        #     event.__class__.__name__
        # )
        
        user: User = data.get("event_from_user")
        
        if not user:
            return await handler(event, data)
            
        user_id = user.id
        
        if event.message:
            if user_id in self.message_cache:
                # logger.debug(f"Throttled message from user: {user_id}")
                return
            self.message_cache[user_id] = True
            
        if event.callback_query:
            if user_id in self.callback_cache:
                # logger.debug(f"Throttled callback from user: {user_id}")
                await event.callback_query.answer(text="⚠️ Не так быстро!", show_alert=True)
                return
            self.callback_cache[user_id] = True
        
        result = await handler(event, data)
        # logger.debug('Выходим из миддлвари  %s', __class__.__name__)
        return result
    
    