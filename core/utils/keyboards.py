from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

def get_language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("language_english", DEFAULT_LANGUAGE))],
            [KeyboardButton(text=get_text("language_german", DEFAULT_LANGUAGE))],
            [KeyboardButton(text=get_text("language_russian", DEFAULT_LANGUAGE))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_post_results_keyboard(language: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("back_to_search_menu", language))],
            [KeyboardButton(text=get_text("back_to_main_menu", language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )