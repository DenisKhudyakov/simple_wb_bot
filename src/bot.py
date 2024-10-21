from aiogram import Bot, Dispatcher

from src.config import TELEGRAM_TOKEN
from src.handlers import router

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)
