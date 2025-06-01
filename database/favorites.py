# from aiogram import Router, types, F
# from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.fsm.context import FSMContext
# from utils.db import add_to_favorites, remove_from_favorites, get_user_favorites
# from utils.texts import get_text
# from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES

# router = Router()

# @router.callback_query(F.data.startswith("addfav_"))
# async def handle_add_favorite(callback: types.CallbackQuery):
#     movie_id = int(callback.data.split("_")[1])
#     user_id = callback.from_user.id

#     success = add_to_favorites(user_id, movie_id)
#     if success:
#         await callback.answer("⭐ Добавлено в избранное")
#     else:
#         await callback.answer("❌ Ошибка при добавлении")


# @router.message(F.text.in_([
#     get_text("favorites", lang) for lang in AVAILABLE_LANGUAGES
# ]))
# async def show_favorites(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     language = data.get("language", DEFAULT_LANGUAGE)

#     user_id = message.from_user.id
#     favorites = get_user_favorites(user_id)

#     if not favorites:
#         await message.answer(get_text("no_favorites", language))
#         return

#     for movie_id, title, year, rating in favorites:
#         text = f"🎬 <b>{title}</b> ({year})\n⭐️ {rating}"
#         keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
#             [types.InlineKeyboardButton(text=get_text("remove_from_favorites", language), callback_data=f"delfav_{movie_id}")]
#         ])
#         await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
