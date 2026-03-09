from sqlalchemy import select, func
from datetime import datetime, timezone

from db.db import SessionLocal
from models.workout_log import WorkoutLog


class WorkoutRepo:
    """Репозиторий для хранения инфо по активности"""

    async def add_workout(self, tg_id, workout_type, minutes, calories):
        """Добавление активности"""

        async with SessionLocal() as session:

            workout = WorkoutLog(
                tg_id=tg_id,
                workout_type=workout_type,
                minutes=minutes,
                calories_burned=calories
            )
            session.add(workout)

            await session.commit()


    async def get_daily_burned(self, tg_id):
        """Получение инфо о потраченных калориях"""

        async with SessionLocal() as session:
            
            daily_dt = datetime.now(timezone.utc).date()

            result = await session.execute(
                select(func.sum(WorkoutLog.calories_burned)).where(
                    WorkoutLog.tg_id == tg_id,
                    func.date(WorkoutLog.created_dt) == daily_dt
                )
            )

            total = result.scalar()

            return total or 0
        

    async def get_daily_minutes(self, tg_id):
        """Получение инфо о времени тренировок для расчёта доп воды"""

        async with SessionLocal() as session:
            
            daily_dt = datetime.now(timezone.utc).date()

            result = await session.execute(
                select(func.sum(WorkoutLog.minutes)).where(
                    WorkoutLog.tg_id == tg_id,
                    func.date(WorkoutLog.created_dt) == daily_dt
                )
            )

            minutes = result.scalar()

            return minutes or 0