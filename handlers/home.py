from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.texts import get_text

def get_post_results_keyboard(language: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("back_to_search_menu", language))],
            [KeyboardButton(text=get_text("back_to_main_menu", language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
