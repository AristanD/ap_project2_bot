from db.base import Base
from db.db import engine


async def init_db():
    """Инициализация БД, не забыть убрать из main"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)