import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_NAME = os.getenv("DB_NAME", "movie_bot")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "movie_bot.log")

AVIAILABLE_LANGUAGES = ["en", "de", "ru"]

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")