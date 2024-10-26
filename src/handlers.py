import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery

import src.keyboard as kb
from src.bd.crud import add_product, clear_product_table, filter_products, \
    get_all_products
from src.config import DEFAULT_COMMANDS
from src.keyboard import cancel_keyboard
from src.service import get_feedbackPoints_and_total_price

router = Router()
cancel_process = False


@router.message(CommandStart())
async def send_chat_product_with_cashback(message: types.Message):
    """Команда старт запускает процесс наполнение БД товарами с кэшбеком"""
    global cancel_process
    cancel_process = False
    await message.answer(
        f"Привет, {message.from_user.full_name}, процесс наполнения базы данных запущен, нажмите /help",
        reply_markup=cancel_keyboard,
    )
    async with aiohttp.ClientSession() as session:
        async for product in get_feedbackPoints_and_total_price(session):
            await add_product(
                name=product["name_product"],
                price=product["total_price"],
                cashback=product["cash_back"],
                url=product["url"],
                sub_category=product["catalog"]["category_name"],
            )
    await message.answer(f"база данных загружена")


@router.message(F.text == "Отмена")
async def cancel_process(message: types.Message):
    """Прерывание наполнения базы данных"""
    global cancel_process
    cancel_process = True
    await message.answer("Процесс остановлен")


@router.message(Command("select_category"))
async def send_category_buttons(message: types.Message):
    """
    Функция вывода кнопок с категориями

    """
    await message.answer(
        "Выберите категорию:", reply_markup=await kb.keyboard_catalog()
    )

"""
Не актуальный хендлер, который обрабатывает кнопки с подкатегориями
"""
# @router.callback_query(lambda call: call.data.startswith("category_"))
# async def callback_inline(call: CallbackQuery):
#     """Функция вывода кнопок с подкатегориями"""
#     CATALOG = await kb.catalog()
#     category = call.data.split("_")[1]
#     subcategories = CATALOG.get(category, [])
#     if subcategories:
#         await call.message.answer(
#             "Выберите подкатегорию:",
#             reply_markup=await kb.sub_catalog_keyboard(category),
#         )
#     else:
#         await call.message.answer(f"Подкатегории для категории {category} не найдены.")


@router.callback_query(lambda call: call.data.startswith("cat_"))
async def callback_product(call: types.CallbackQuery):
    """Функция вывода товаров с кэшбэком через кнопку"""
    subcategory = call.data.split("_")[1]
    products = await filter_products(subcategory)
    if products:
        for product in products:
            await call.message.answer(
                f"Название: {product.name}\nЦена: {product.price}\n"
                f"Баллы: {product.cashback}\nСсылка на товар: {product.url}",
                reply_markup=cancel_keyboard,
            )
    else:
        await call.message.answer(
            "Товары с кэшбэком не найдены в данной категории, либо они ещё не загружены",
            reply_markup=cancel_keyboard
        )


@router.message(Command("clear"))
async def clear(message: types.Message):
    """Очистка базы данных"""
    await message.answer("Очистка базы данных запущена")
    await clear_product_table()
    await message.answer(
        f"База данных очищена, нажмите команду /start, чтобы заполнять базу данных актуальными товарами"
    )


@router.message(Command("help"))
async def help(message: types.Message):
    """Справка"""
    commands = "\n".join([f"{command[0]} - {command[1]}" for command in DEFAULT_COMMANDS])
    await message.answer(f"Инструкция: {commands}")


@router.message(Command("high_cashback"))
async def show_products_with_high_cashback(message: types.Message):
    """Функция для вывода товаров с кэшбэком больше цены"""
    products = await get_all_products()
    if products:
        for product in products:
            await message.answer(
                f"Название: {product.name}\nЦена: {product.price}\n"
                f"Баллы: {product.cashback}\nСсылка на товар: {product.url}"
            )
    else:
        await message.answer("Нет товаров с кэшбэком больше цены")
