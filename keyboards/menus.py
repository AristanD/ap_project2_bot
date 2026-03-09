from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Меню команд
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/set_profile"),
            KeyboardButton(text="/check_progress")
        ],
        [
            KeyboardButton(text="/log_water"),
            KeyboardButton(text="/log_food")
        ],
        [
            KeyboardButton(text="/log_workout")
        ]
    ],
    resize_keyboard=True
)