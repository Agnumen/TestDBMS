import logging
from contextlib import suppress

from aiogram import Bot, Router
from aiogram.enums import BotCommandScopeType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommandScopeChat, ChatMemberUpdated, Message

from app.bot.keyboards.menu_button import get_main_menu_commands
from app.bot.states.states import LangSG

from app.core.enums import UserRole
from app.core.schemas import UserCreateDTO, UserUpdateDTO

from app.infrastructure.database import Database

logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
user_router = Router()


# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart())
async def process_start_command(
    msg: Message, 
    db: Database, 
    bot: Bot, 
    i18n: dict[str, str], 
    state: FSMContext, 
    admin_ids: set[int],
    translations: dict
):
    user = await db.user.get_by_id(user_id=msg.from_user.id)
    
    # OLD user = await UserDAO.find_one_or_none(session=session, filters=UserUpdate(user_id=msg.from_user.id))
    if user is None:
        user_role = UserRole.ADMIN if msg.from_user.id in admin_ids else UserRole.USER
        
        # OLD
        # await UserDAO.add_one(session=session, values=UserCreate(
        #     user_id=msg.from_user.id,
        #     username=msg.from_user.username,
        #     first_name=msg.from_user.first_name,
        #     last_name=msg.from_user.last_name,
        #     language=msg.from_user.language_code or "ru",
        #     role=user_role
        # ))
        
        await db.user.create_user(user_data=UserCreateDTO(
            user_id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name,
            language=msg.from_user.language_code or "ru",
            role=user_role,
        ))
        
    else:
        
        user_role = UserRole(user.role)
        
        # OLD
        # await UserDAO.update_one_by_id(session=session, 
        #     data_id=user.id,
        #     values=UserUpdate(is_alive=True)
        # )
        # NEW
        await db.user.change_alive_status(
            user_id=msg.from_user.id,
            is_alive=True,
        )
        

    if await state.get_state() == LangSG.lang:
        data = await state.get_data()
        with suppress(TelegramBadRequest):
            msg_id = data.get("lang_settings_msg_id")
            if msg_id:
                await bot.edit_message_reply_markup(chat_id=msg.from_user.id, message_id=msg_id)
        # OLD
        # user_lang = await UserDAO.get_user_lang(session=session, user_id=msg.from_user.id)
        # NEW
        user_lang = await db.user.get_user_language(user_id=msg.from_user.id)
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
async def process_user_blocked_bot(event: ChatMemberUpdated, db: Database):
    logger.info("User %d has blocked the bot", event.from_user.id)
    # old
    # await UserDAO.change_user_alive_status(session=session, user_id=event.from_user.id, is_alive=False)
    
    # NEW
    await db.user.change_alive_status(user_id=event.from_user.id, is_alive=False)


# Временный хендлер для проверки /del
@user_router.message(Command(commands="del"))
async def process_del_command(msg: Message, db: Database):
    await db.user.delete_user(user_id=msg.from_user.id)