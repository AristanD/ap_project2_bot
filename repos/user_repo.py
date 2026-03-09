from sqlalchemy import select

from db.db import SessionLocal
from models.user import User


class UserRepo:
    """Класс для запроса состояний конкретного пользователя"""

    async def create_update(self, tg_id: int, data: dict):
        """Создание или обновления инфо пользователя"""

        async with SessionLocal() as session:
            result = await session.execute(
                select(User).where(User.id == tg_id)    # Ищу пользователя в таблице по его айдишнику
                )
            
            user = result.scalar_one_or_none()

            if user is None:    # Если пользователь не найден, добавляю его айдишник
                user = User(tg_id=tg_id, **data)
                session.add(user)

            else:
                for key, val in data.items():
                    setattr(user, key, val)     # Добавляю новую строку по имеющемуся ID

            await session.commit()  # Коммит - сохранение нового инфо

    
    async def get_tg_id(self, tg_id: int):
        """Получение инфо пользователя по tg-id"""

        async with SessionLocal() as session:
            result = await session.execute(select(User).where(User.tg_id == tg_id))

        return result.scalar_one_or_none()