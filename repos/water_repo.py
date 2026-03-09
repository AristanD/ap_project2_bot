from sqlalchemy import select, func
from datetime import datetime, timezone

from db.db import SessionLocal
from models.water_log import WaterLog


class WaterRepo:
    """Репозиторий для воды"""

    async def add_log(self, tg_id: int, amt: int):
        """Добавление логов воды"""

        async with SessionLocal() as session:
            log = WaterLog(
                tg_id=tg_id,
                amt_ml=amt
            )

            session.add(log)
            await session.commit()

    
    async def get_daily_total(self, tg_id: int):
        """Получение общего объёма выпитого за день"""
        async with SessionLocal() as session:

            daily_dt = datetime.now(timezone.utc).date()
            result = await session.execute(
                select(func.sum(WaterLog.amt_ml)).where(
                    WaterLog.tg_id == tg_id,
                    func.date(WaterLog.created_dt) == daily_dt
                )   # Сумма по конкретному пользователю за сутки
            )

            total = result.scalar()

            return total or 0