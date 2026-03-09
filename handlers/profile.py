from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from schemas.profile import ProfileStates
from services.calories_service import CaloriesService
from services.weather_service import WeatherService
from services.water_service import WaterService
from repos.user_repo import UserRepo


router = Router()

user_repo = UserRepo()


@router.message(Command("set_profile"))
async def start_profile_setup(message: Message, state: FSMContext):
    """Ручка старта функции добавления инфо о пользователе (срабатывает после команды /set_profile)"""

    await message.answer("🏋️ Укажите вас вес (в кг):")
    await state.set_state(ProfileStates.weight)


@router.message(ProfileStates.weight)   # Срабатывает после получения инфо о весе
async def process_weight(message: Message, state: FSMContext):
    """Ручка для добавления роста пользователя и обработки веса (срабатывает после start_profile_setup)"""

    await state.update_data(weight=int(message.text))

    await message.answer("📏 Укажите ваш рост (в см):")
    await state.set_state(ProfileStates.height)


@router.message(ProfileStates.height)   # Срабатывает после получения инфо о росте
async def process_height(message: Message, state: FSMContext):
    """Ручка для добавления возраста пользователя и обработки роста (срабатывает после process_weight)"""
    await state.update_data(height=int(message.text))

    await message.answer("👴 Укажите ваш возраст (полных лет):")
    await state.set_state(ProfileStates.age)


@router.message(ProfileStates.age)  # Срабатывает после получения инфо о возрасте
async def process_age(message: Message, state: FSMContext):
    """Ручка для добавления времени активности пользователя и обработки возраста (срабатывает после process_height)"""

    await state.update_data(age=int(message.text))

    await message.answer("🤸 Сколько времени за день вы проводите в активном состоянии (в минутах)?")
    await state.set_state(ProfileStates.activity)


@router.message(ProfileStates.activity)
async def process_activity(message: Message, state: FSMContext): # Срабатывает после получения инфо о времени активности
    """Ручка для добавления локации пользователя и обработки времени активности (срабатывает после process_age)"""

    await state.update_data(activity_time=int(message.text))

    await message.answer("🏙️ В каком городе вы живёте?")
    await state.set_state(ProfileStates.city)


@router.message(ProfileStates.city) # Срабатывает после получения инфо о городе
async def process_city(message: Message, state: FSMContext):
    """Ручка для добавления цели по калориям и обработки локации (срабатывает после process_age)"""
    await state.update_data(city=message.text)

    await message.answer(
        "Сколько калорий за день вы хотите тратить (в минутах)? \n\n"
        "Если не знаете, то напишите 'Не знаю':"
    )
    await state.set_state(ProfileStates.calorie_goal)


@router.message(ProfileStates.calorie_goal)
async def process_calorie_goal(message: Message, state: FSMContext):
    """Ручка для обработки цели по калориям и завершения формирования инфо о пользователе"""

    data = await state.get_data()

    weight = data["weight"]
    height = data["height"]
    age = data["age"]
    activity = data["activity_time"]
    city = data["city"]

    if message.text.lower() == "не знаю":
        calories = CaloriesService.calc_daily_calories(
            weight,
            height,
            age,
            activity
        )   # Авто расчёт дневной нормы по калориям
    else:
        calories = int(message.text)

    temp = await WeatherService.get_temp(city)
    water_goal = WaterService.calc_water_goal(
        weight,
        activity,
        temp
    )

    profile_data = {
        "weight": weight,
        "height": height,
        "age": age,
        "activity_time": activity,
        "city": data["city"],
        "calorie_goal": calories,
        "water_goal": water_goal
    }

    await user_repo.create_update(
        tg_id=message.from_user.id,
        data=profile_data
    )

    await message.answer(
        f"✅ Ваш профиль сохранён!\n"
        f"🔥 Ваша дневная норма калорий: {calories} ккал\n"
        f"🫗 Ваша норма воды: {water_goal} мл"
    )

    await state.clear()