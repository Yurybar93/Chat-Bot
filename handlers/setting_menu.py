from aiogram import Router, types
from utils.texts import get_text

router = Router()

def get_settings_menu(language: str) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=get_text("change_language", language))],
            [types.KeyboardButton(text=get_text("back_to_main_menu", language))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
