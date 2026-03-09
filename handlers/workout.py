from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from repos.user_repo import UserRepo
from repos.workout_repo import WorkoutRepo
from services.workout_service import WorkoutService


router = Router()

user_repo = UserRepo()
workout_repo = WorkoutRepo()


@router.message(Command("log_workout"))
async def log_workout(message: Message):
    """Ручка для получения инфо об активности пользователя"""

    args = message.text.split()
    if len(args) < 3:
        await message.answer(
            "❌ Неверно введена команда\n\nДля отслеживания активности введите\n"
            "/log_workout <тип> <минуты>\n\n\n"
            "Доступные типы: running, cycling, swimming, walking, gym"
        )
        return
    
    workout_type = args[1].lower()
    minutes = int(args[2])

    user = await user_repo.get_tg_id(message.from_user.id)

    calories = WorkoutService.calc_calories(workout_type, minutes)
    water_bonus = WorkoutService.additional_water(minutes)

    await workout_repo.add_workout(
        user.id,
        workout_type,
        minutes,
        calories
    )

    await message.answer(
        f"👟 Ваша активность записана\n\n"
        f"Тип активности: {workout_type}\n"
        f"Время активности: {minutes} мин\n"
        f"🔥 Сожжено: {calories} ккал\n"
        f"🫗 Дополнительно выпейте: {water_bonus} мл воды"
    )