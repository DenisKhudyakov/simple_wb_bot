from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,
)
