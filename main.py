import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import start, profile, water, food, workout, progress
from logs.logging import Logging

from db.init_db import init_db


bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # Инит бота
storage = MemoryStorage()   # Место хранения БД
dp = Dispatcher()   # Диспетчер обновлений для управления логикой бота


async def main():
    """Запуск бота"""
    await init_db()

    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(water.router)
    dp.include_router(food.router)
    dp.include_router(workout.router)
    dp.include_router(progress.router)

    dp.message.middleware(Logging())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())