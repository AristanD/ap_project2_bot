from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from repos.user_repo import UserRepo
from repos.water_repo import WaterRepo
from services.weather_service import WeatherService
from services.water_service import WaterService


router = Router()

user_repo = UserRepo()
water_repo = WaterRepo()


@router.message(Command("log_water"))
async def log_water(message: Message):
    """Ручка для учёта воды"""

    args = message.text.split()

    if len(args) < 2:
        await message.answer("🫗 Не распознаны введённые данные\n\n"
                             "Чтобы точно задать объём выпитого используйте команду /log_water число")
        return
    
    amt = int(args[1])
    user = await user_repo.get_tg_id(message.from_user.id)

    if not user:
        await message.answer("🫷 Вас нет в системе!\n\nСначала создайте свой профиль с помощью команды /set_profile")
        return
    
    await water_repo.add_log(user.id, amt)

    daily_total = await water_repo.get_daily_total(user.id)
    temp = await WeatherService.get_temp(user.city)

    goal = WaterService.calc_water_goal(
        user.weight,
        user.activity_time,
        temp
    )

    daily_remain = max(goal - daily_total, 0)

    await message.answer(
        f"🫗 Принято: {amt} мл\n\n"
        f"Принято за сегодня: {daily_total} мл\n"
        f"Цель: {goal} мл\n"
        f"Осталось выпить: {daily_remain} мл\n"
        f"Температура сегодня в {user.city}: {temp}°C \n\n\n !!! Важно !!! \nПри температуре выше 25°C ваша дневная норма воды будет увеличена"
    )