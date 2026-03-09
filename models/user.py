from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class User(Base):
    """Класс для создания БД с ключом ID пользователя"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)    # тг адишник отделил от основного

    weight: Mapped[int]
    height: Mapped[int]
    age: Mapped[int]

    activity_time: Mapped[int]

    city: Mapped[str]

    calorie_goal: Mapped[int]
    water_goal: Mapped[int]