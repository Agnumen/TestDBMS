from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dao.dao import UserDAO
from app.infrastructure.database.schemas import UserCreate
from app.infrastructure.database.enums import UserRole
from app.infrastructure.database.dao.session_maker import connection

others_router = Router()

async def hello(msg: Message, session: AsyncSession):
    user_data = UserCreate(
        user_id = msg.from_user.id,
        username = msg.from_user.username,
        first_name = msg.from_user.first_name,
        last_name=msg.from_user.last_name,
        role=UserRole.USER,
    )
    await UserDAO.add_one(session=session, values=user_data)
    
# OR

@others_router.message(CommandStart())
@connection()
async def hellov2(msg: Message, session: AsyncSession):
    
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    user_data = {
        "user_id": msg.from_user.id,
        "username": msg.from_user.username,
        "first_name": first_name if len(first_name) > 2 else "No First Name",
        "last_name":last_name if last_name is not None else "No Last Name",
        "language": msg.from_user.language_code,
        "role": UserRole.USER,
        "is_alive": True,
        "banned": False,
    }
    
    validated_data = UserCreate(**user_data)
        
    user = await UserDAO.add_one(user_data=validated_data)
    print(user)
    await msg.answer(f"Привет, {user.first_name}! Твой ID: {user.id}")
    

@others_router.message()
async def send_echo(message: Message, session: AsyncSession):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="No echo")