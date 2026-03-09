from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from repos.user_repo import UserRepo
from repos.food_repo import FoodRepo
from services.food_service import FoodService
from schemas.food_states import FoodStates


router = Router()

user_repo = UserRepo()
food_repo = FoodRepo()


@router.message(Command("log_food"))
async def log_food(message: Message, state: FSMContext):
    """Ручка для получения инфо о типе съеденной пользователем еды"""

    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("🍕 Не распознаны введённые данные о еде\n"
                             "Чтобы указать объём съеденной еды, используйте команду '/log_food название продукта'")
        return
    
    product_name = args[1]
    product = await FoodService.search_product(product_name)

    if not product:
        await message.answer("❌ Информация о продукте не найдена")
        return
    
    await state.update_data(product=product)
    await message.answer(
        f"✅ Продукт найдет {product['name']} — {product['calories_100g']} ккал на 100 грамм\n"
        f"Укажите сколько вы съели:"
    )

    await state.set_state(FoodStates.waiting_gramms)


@router.message(FoodStates.waiting_gramms)
async def processing_gramms(message: Message, state: FSMContext):

    gramms = int(message.text)
    data = await state.get_data()
    
    product = data["product"]
    calories = product["calories_100g"] * gramms / 100

    user = await user_repo.get_tg_id(message.from_user.id)

    await food_repo.add_log(
        user.id,
        product["name"],
        gramms,
        calories
    )
    await message.answer(
        f"✅ Принято:\n"
        f"🍕 {product['name']} — {gramms} грамм\n"
        f"🔥 {calories:.1f} ккал"
    )

    await state.clear()