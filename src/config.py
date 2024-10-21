import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("No .env file found")
else:
    load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
