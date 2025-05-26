from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from utils.texts import get_text
from config import AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE
from handlers.search_menu import get_search_menu
router = Router()

all_main_menu_texts = []
for lang_code in AVAILABLE_LANGUAGES:
    all_main_menu_texts.extend([
        get_text("find_movie", lang_code),
        get_text("favorites", lang_code),
        get_text("settings", lang_code),
    ])

@router.message(F.text.in_(all_main_menu_texts))
async def handle_main_menu(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", DEFAULT_LANGUAGE)

    if message.text == get_text("find_movie", language):
        await message.answer(get_text("search_prompt", language),
                             reply_markup=get_search_menu(language))
    elif message.text == get_text("favorites", language):
        await message.answer(get_text("favorites_list", language))
    elif message.text == get_text("settings", language):
        await message.answer(get_text("settings_menu", language))
