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
            [types.KeyboardButton(text=get_text("back_to_main_menu", language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

@router.message()
async def show_search_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)
    expected_text = "🔍 " + get_text("find_movie", language)

    if message.text == expected_text:
        await message.answer(
            get_text("search_prompt", language),
            reply_markup=get_search_menu(language)
        )
    elif message.text == get_text("back_to_main_menu", language):
        await message.answer(
            get_text("back_to_main_menu_prompt", language),
            reply_markup=get_search_menu(language)
        )
