import logging
from contextlib import suppress

from pydantic import create_model, Field

from aiogram import Bot, Router
from aiogram.enums import BotCommandScopeType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommandScopeChat, ChatMemberUpdated, Message

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.menu_button import get_main_menu_commands
from app.bot.states.states import LangSG
from app.infrastructure.database.enums import UserRole
from app.infrastructure.database.dao.dao import UserDAO
from app.infrastructure.database.dao.session_maker import connection
from app.infrastructure.database.schemas import UserCreate, UserUpdate



logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
user_router = Router()


# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart())
@connection()
async def process_start_command(
    msg: Message, 
    session: AsyncSession, 
    bot: Bot, 
    i18n: dict[str, str], 
    state: FSMContext, 
    admin_ids: list[int],
    translations: dict
):
    
    user = await UserDAO.find_one_or_none(session=session, filters=UserUpdate(user_id=msg.from_user.id))
    if user is None:
        user_role = UserRole.ADMIN if msg.from_user.id in [admin_ids] else UserRole.USER
        
        await UserDAO.add_one(session=session, values=UserCreate(
            user_id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name,
            language=msg.from_user.language_code or "ru",
            role=user_role
        ))
        
    else:
        
        user_role = UserRole(user.role)
        
        await UserDAO.update_one_by_id(session=session, 
            data_id=user.id,
            values=UserUpdate(is_alive=True)
        )
        

    if await state.get_state() == LangSG.lang:
        data = await state.get_data()
        with suppress(TelegramBadRequest):
            msg_id = data.get("lang_settings_msg_id")
            if msg_id:
                await bot.edit_message_reply_markup(chat_id=msg.from_user.id, message_id=msg_id)
        user_lang = await UserDAO.get_user_lang(session=session, user_id=msg.from_user.id)
        i18n = translations.get(user_lang)
    
    await bot.set_my_commands(
        commands=get_main_menu_commands(i18n=i18n, role=user_role),
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT,
            chat_id=msg.from_user.id
        )
    )

    await msg.answer(text=i18n.get("/start"))
    await state.clear()


# Этот хэндлер срабатывает на команду /help
@user_router.message(Command(commands="help"))
async def process_help_command(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get("/help"))


# Этот хэндлер будет срабатывать на блокировку бота пользователем
@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
@connection()
async def process_user_blocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    logger.info("User %d has blocked the bot", event.from_user.id)
    await UserDAO.change_user_alive_status(session=session, user_id=event.from_user.id, is_alive=False)
