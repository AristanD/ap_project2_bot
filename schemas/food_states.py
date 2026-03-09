from aiogram.fsm.state import State, StatesGroup


class FoodStates(StatesGroup):
    """Состояния каллорийности еды"""
    waiting_gramms = State()