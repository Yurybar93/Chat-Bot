from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from core.database.favorites import get_user_favorites
from core.utils.texts import get_text
from core.services.search_service import format_movie_preview
from config import AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE

router = Router()

@router.message(F.text.in_([
    get_text("favorites", lang) for lang in AVAILABLE_LANGUAGES
]))
async def show_favorites(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    favorites = get_user_favorites(user_id)

    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)

    if not favorites:
        await message.answer(get_text("no_favorites", language))
        return

    for movie_id, title, year, rating in favorites:
        msg = format_movie_preview(title, year, rating)
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text=get_text("remove_from_favorites", language),
                callback_data=f"delfav_{movie_id}"
            )]
        ])
        await message.answer(msg, parse_mode="HTML", reply_markup=keyboard)
