from aiogram.fsm.state import State, StatesGroup


class ProfileStates(StatesGroup):
    """Класс-схема для состояний пользователя"""

    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()
    calorie_goal = State()
    water_goal = State()