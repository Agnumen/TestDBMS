import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User
from app.infrastructure.database.dao.dao import UserDAO
from app.infrastructure.database.dao.session_maker import connection_cl
logger = logging.getLogger(__name__)

class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)
        
        state: FSMContext = data.get('state')
        user_context_data = await state.get_data()

        if (user_lang := user_context_data.get('user_lang')) is None:
            
            # session
            # тут был метод когда conn бралось из workflow_data 
            # if  is None:
            #     logger.error("Database connection not found in middleware data.")
            #     raise RuntimeError("Missing database connection for detecting the user's language.")

            # user_lang: str | None = await UserDAO.get_user_lang(session=session, user_id=user.id)
            # if user_lang is None:
            user_lang = user.language_code

        translations: dict = data.get("translations")
        i18n: dict = translations.get(user_lang)

        if i18n is None:
            data["i18n"] = translations[translations["default"]]
        else:
            data["i18n"] = i18n

        return await handler(event, data)