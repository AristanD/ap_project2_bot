from sqlalchemy import select, func
from datetime import datetime, timezone

from db.db import SessionLocal
from models.food_log import FoodLog


class FoodRepo:
    """Репозиторий для хранения данных о еде"""

    async def add_log(self, tg_id, product, gramms, calories):
        """Добавление логов по еде"""
        async with SessionLocal() as session:

            log = FoodLog(
                tg_id=tg_id,
                product_name=product,
                gramms=gramms,
                calories=calories
            )
            session.add(log)

            await session.commit()

        
    async def get_daily_calories(self, tg_id):
        """Дневная норма калорий"""
        async with SessionLocal() as session:

            daily = datetime.now(timezone.utc).date()
            result = await session.execute(
                select(func.sum(FoodLog.calories)).where(
                    FoodLog.tg_id == tg_id,
                    func.date(FoodLog.created_dt) == daily
                )
            )

            total = result.scalar()

            return total or 0