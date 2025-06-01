from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from utils.db import add_to_favorites, remove_from_favorites, get_user_favorites
from utils.texts import get_text
from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES

router = Router()

@router.callback_query(F.data.startswith("addfav_"))
async def handle_add_favorite(callback: types.CallbackQuery, state: FSMContext):
    movie_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    # Язык из состояния (если есть), иначе по умолчанию
    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)

    success = add_to_favorites(user_id, movie_id)
    if success:
        await callback.answer(get_text("added_to_favorites", language))
    else:
        await callback.answer(get_text("add_to_favorites_error", language))


@router.message(F.text.in_([
    get_text("favorites", lang) for lang in AVAILABLE_LANGUAGES
]))
async def show_favorites(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)

    user_id = message.from_user.id
    favorites = get_user_favorites(user_id)

    if not favorites:
        await message.answer(get_text("no_favorites", language))
        return

    for movie_id, title, year, rating in favorites:
        text = f"🎬 <b>{title}</b> ({year})\n⭐️ {rating}"
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=get_text("remove_from_favorites", language), callback_data=f"delfav_{movie_id}")]
        ])
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

@router.callback_query(F.data.startswith("delfav_"))
async def handle_remove_favorite(callback: types.CallbackQuery, state: FSMContext):
    movie_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)

    success = remove_from_favorites(user_id, movie_id)
    if success:
        await callback.answer(get_text("removed_from_favorites", language))
        await callback.message.delete()  
    else:
        await callback.answer(get_text("remove_from_favorites_error", language))


