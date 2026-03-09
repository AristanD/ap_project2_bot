from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from repos.user_repo import UserRepo
from repos.water_repo import WaterRepo
from repos.food_repo import FoodRepo
from repos.workout_repo import WorkoutRepo
from services.workout_service import WorkoutService


router = Router()

user_repo = UserRepo()
water_repo = WaterRepo()
food_repo = FoodRepo()
workout_repo = WorkoutRepo()


@router.message(Command("check_progress"))
async def check_progress(message: Message):
    """Ручка для проверки текущего прогресса (ежедневно)"""

    user = await user_repo.get_tg_id(message.from_user.id)
    if not user:
        await message.answer("Ваш профиль не найден!\nВведите команду /set_profile и настройте профиль")
        return
    
    water = await water_repo.get_daily_total(user.id)
    calories_in = await food_repo.get_daily_calories(user.id)
    calories_out = await workout_repo.get_daily_burned(user.id)
    workout_minutes = await workout_repo.get_daily_minutes(user.id)
    water_bonus = WorkoutService.additional_water(workout_minutes)
    water_goal = user.water_goal + water_bonus
    water_remain = max(water_goal - water, 0)
    calories_balance = calories_in - calories_out

    await message.answer(
        f"📊 Прогресс\n\n"

        f"🫗 Вода\n"
        f"Выпито: {water} / {water_goal} мл\n"
        f"Осталось: {water_remain} мл\n"
        f"Бонус за тренировки: +{water_bonus} мл\n\n"

        f"🍕 Калории\n"
        f"Съедено: {calories_in:.1f} / {user.calorie_goal}\n"
        f"Сожжено: {calories_out}\n"
        f"Итого: {calories_balance:.1f}"
    )