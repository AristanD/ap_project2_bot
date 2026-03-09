import os
from dotenv import load_dotenv

load_dotenv()   #  Загрузка переменных виртуального окружения


class Config:
    """Конфиг, который принимает токен из .env и url расположения БД (SQL LITE)"""
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DB_URL = "sqlite+aiosqlite:///bot.db"

    OWM_API_KEY = os.getenv("OWM_API_KEY")


config = Config()