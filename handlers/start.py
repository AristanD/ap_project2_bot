from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.menus import main_menu


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):  # Стартовое приветствие и инфо от бота
    await message.answer(
        "Здравствуйте!\n"
        "Вы обратились к боту для отслеживания:\n\n"
        "🫗 воды\n"
        "🍕 калорий\n"
        "👟 тренировок\n\n\n"
        "⚙️ Введите команду /set_profile для начала работы:",
        reply_markup=main_menu
    )