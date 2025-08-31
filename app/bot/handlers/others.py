from aiogram import Router
from aiogram.types import Message

others_router = Router()

@others_router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="No echo")