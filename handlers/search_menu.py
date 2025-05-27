from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from utils.texts import get_text
from config import DEFAULT_LANGUAGE

router = Router()

def get_search_menu(language: str) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=get_text("search_by_genre_year", language))],
            [types.KeyboardButton(text=get_text("search_by_title", language))],
            [types.KeyboardButton(text=get_text("search_by_keyword", language))],
            [types.KeyboardButton(text=get_text("search_popular", language))],
            [types.KeyboardButton(text=get_text("back_to_main_menu", language))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

@router.message(F.text == get_text("back_to_main_menu", DEFAULT_LANGUAGE))
async def handle_back_to_main_menu(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language", DEFAULT_LANGUAGE)
    await message.answer(get_text("back_to_main_menu_prompt", language),
                         reply_markup=get_search_menu(language))

