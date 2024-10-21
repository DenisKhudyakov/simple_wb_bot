import aiohttp
from aiogram import F, Router, types
from aiogram.filters import CommandStart

from src.keyboard import cancel_keyboard
from src.service import get_feedbackPoints_and_total_price

router = Router()
cancel_process = False


@router.message(CommandStart())
async def send_chat_product_with_cashback(message: types.Message):
    global cancel_process
    cancel_process = False

    async with aiohttp.ClientSession() as session:
        async for catalog in get_feedbackPoints_and_total_price(session):
            if cancel_process:
                await message.answer(
                    "Процесс прерван. чтобы запустить бота введите /start"
                )
                break
            if catalog:
                await message.answer(
                    f"Название: {catalog["name_product"]}\nЦена: {catalog["total_price"]}\n"
                    f"Баллы: {catalog["cash_back"]}\nСсылка на товар: {catalog["url"]}",
                    reply_markup=cancel_keyboard,
                )


@router.message(F.text == "Отмена")
async def cancel_process(message: types.Message):
    global cancel_process
    cancel_process = True
    await message.answer("Процесс остановлен")
