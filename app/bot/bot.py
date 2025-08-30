import asyncio
import logging
# import os.path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from app.bot.i18n import get_translations
from app.bot.handlers import others, user
from app.bot.middlewares import TranslatorMiddleware

from config import Settings
# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main(config: Settings): 

    logging.basicConfig(
        level=config.LOG_LEVEL,
        format=config.LOG_FORMAT,
    )
    
    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")
    
    # Инициализируем объект хранилища
    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB_NUM,
        username=config.REDIS_USERNAME,
        password=config.REDIS_PASSWORD
    )
    storage = RedisStorage(redis=redis)
    
    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="html")
    )
    dp = Dispatcher(storage=storage)

    # Инициализируем другие объекты (пул соединений с БД, кеш и т.п.)
    # Инициализируем движок и сессию для работы с базой данных

    engine = create_async_engine(url=config.get_db_url()) # , echo=True)
    session = async_sessionmaker(engine, expire_on_commit=False)

    # Настраиваем главное меню бота
    # await set_main_menu(bot)
    
    # Получаем словарь с переводами
    translations = get_translations()
    # формируем список локалей из ключей словаря с переводами
    locales = list(translations.keys())

    # Помещаем нужные объекты в workflow_data диспетчера
    dp.workflow_data.update({
        "admin_ids": config.BOT_ADMIN_IDS,
        "provider_token": config.BOT_PAYMENT_TOKEN,
        "translations": translations,
        "locales": locales,
        # "banned_storage": banned_storage,
    })
    
    # Подключаем роутеры в нужном порядке
    logger.info("Including routers...")
    # dp.include_routers(settings_router, admin_router, user_router, others_router)
    dp.include_router(user.user_router)
    dp.include_router(others.others_router)

    # Подключаем миддлвари в нужном порядке
    logger.info("Including middlewares...")
    # dp.update.middleware(DataBaseMiddleware())
    # dp.update.middleware(ShadowBanMiddleware())
    # dp.update.middleware(ActivityCounterMiddleware())
    # dp.update.middleware(LangSettingsMiddleware())
    dp.update.middleware(TranslatorMiddleware())
    
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)