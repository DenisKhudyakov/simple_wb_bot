from itertools import chain

from aiogram.types import (InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.service import get_categories

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,
)


async def catalog():
    return await get_categories()


async def keyboard_catalog():
    """Клавиатура для выбора каталога"""
    CATALOG = await catalog()
    keyboard = InlineKeyboardBuilder()
    for cat in CATALOG.keys():
        keyboard.add(InlineKeyboardButton(text=cat, callback_data=f"category_{cat}"))
    return keyboard.adjust(1).as_markup()


async def sub_catalog_keyboard(catalog_name: str):
    """Клавиатура для выбора подкаталога с обработкой вложенных подкатегорий"""
    CATALOG = await catalog()
    keyboard = InlineKeyboardBuilder()
    sub_catalog = CATALOG.get(catalog_name, [])

    for sub_cat in sub_catalog:
        if isinstance(sub_cat, dict):
            # Если подкатегория - это словарь, получаем подкатегории из его значений
            for sub_cat_name, sub_sub_cat in sub_cat.items():
                if isinstance(sub_sub_cat, list):
                    # Если значение словаря - это список, рекурсивно обработаем его
                    for sub_sub_cat_name in sub_sub_cat:
                        keyboard.add(
                            InlineKeyboardButton(
                                text=sub_sub_cat_name if isinstance(sub_sub_cat_name, str) else sub_cat_name,
                                callback_data=f"subcat_{sub_sub_cat_name[:15] if isinstance(sub_sub_cat_name, str) else sub_cat_name[:15]}"
                            )
                        )
                else:
                    # Если это строка, добавляем ее как подкатегорию
                    keyboard.add(
                        InlineKeyboardButton(
                            text=sub_cat_name,
                            callback_data=f"subcat_{sub_cat_name[:15]}"
                        )
                    )
        else:
            # Если подкатегория - это строка (конечная категория), добавляем ее напрямую
            keyboard.add(
                InlineKeyboardButton(
                    text=sub_cat,
                    callback_data=f"subcat_{sub_cat[:15]}"
                )
            )

    return keyboard.adjust(2).as_markup()





