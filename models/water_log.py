from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class WaterLog(Base):
    """Класс для управления логами воды"""

    __tablename__ = "water_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    amt_ml: Mapped[int]

    created_dt:  Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))