from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class FoodLog(Base):
    """Логирование еды (таблица)"""

    __tablename__ = "food_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    product_name: Mapped[str]
    calories: Mapped[float]
    gramms: Mapped[int]

    created_dt: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
