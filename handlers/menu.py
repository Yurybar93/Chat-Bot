from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from utils.texts import get_text
from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES
from handlers.search_menu import get_search_menu
from handlers.setting_menu import get_settings_menu

router = Router()

@router.message(F.text.in_([
    get_text("find_movie", lang) for lang in AVAILABLE_LANGUAGES
] + [
    get_text("favorites", lang) for lang in AVAILABLE_LANGUAGES
] + [
    get_text("settings", lang) for lang in AVAILABLE_LANGUAGES
]))
async def handle_main_menu_buttons(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)
    text = message.text

    if text == get_text("find_movie", language):
        await message.answer(get_text("search_prompt", language),
                             reply_markup=get_search_menu(language))

    elif text == get_text("favorites", language):
        await message.answer(get_text("favorites_list", language))

    elif text == get_text("settings", language):
        await message.answer(get_text("settings_menu", language),
                             reply_markup=get_settings_menu(language))

