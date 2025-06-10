from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES
from handlers.menu.search_menu import get_search_menu
from handlers.menu.settings_menu import get_settings_menu
from core.database.favorites import get_user_favorites
from core.services.search_service import format_movie_preview

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
        await message.answer(
            get_text("search_prompt", language),
            reply_markup=get_search_menu(language)
        )

    elif text == get_text("favorites", language):
        favorites = get_user_favorites(message.from_user.id)

        if not favorites:
            await message.answer(get_text("no_favorites", language))
        else:
            for movie_id, title, year, rating in favorites:
                msg = format_movie_preview(title, year, rating)
                btn = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text=get_text("remove_from_favorites", language),
                                                callback_data=f"delfav_{movie_id}")]
                ])
                await message.answer(msg, parse_mode="HTML", reply_markup=btn)

    elif text == get_text("settings", language):
        await message.answer(
            get_text("settings_menu", language),
            reply_markup=get_settings_menu(language)
        )

