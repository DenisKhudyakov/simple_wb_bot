import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

if not find_dotenv():
    exit("No .env file found")
else:
    load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
USERNAME_BD = os.getenv("USERNAME_BD")
PASSWORD_BD = os.getenv("PASSWORD_BD")
DB_NAME = os.getenv("DB_NAME")
PORT_BD = os.getenv("PORT_BD")

DATABASE_URL = (
    f"postgresql+asyncpg://{USERNAME_BD}:{PASSWORD_BD}@db:{PORT_BD}/{DB_NAME}"
)
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

DEFAULT_COMMANDS = (
    ("/start", "Запуск бота или перезагрузка бота, наполнение базы данных"),
    (
        "/clear",
        "Очистка таблицы с товарами, т.к. товары с кэшбэком регулярно обновляются",
    ),
    (
        "Кнопка 'Отмена'",
        "Прерывает наполнение базы данных",
    ),
    (
        "/select_category",
        "Выводит список категорий WB",
    ),
    ("Автор бота", "@adv_mf0"),
    ("/high_cashback", "Товары с кэшбэком больше стоимости товара")
)
