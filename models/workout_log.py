from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class WorkoutLog(Base):
    """Логгирование тренировок (таблица)"""

    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    workout_type: Mapped[int] = mapped_column(ForeignKey("users.id"))
    minutes: Mapped[str]
    calories_burned: Mapped[int]

    created_dt: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))