import aiohttp
from aiogram import Bot, Dispatcher

from src.bd.base import create_tables
from src.config import TELEGRAM_TOKEN
from src.handlers import router

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


async def start_bot():
    await create_tables()


async def main():
    dp.include_router(router)
    dp.startup.register(start_bot)
    await dp.start_polling(bot, skip_updates=True)
