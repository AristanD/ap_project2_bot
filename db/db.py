from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import config


engine = create_async_engine(config.DB_URL)

# Создание локальной сессии
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)