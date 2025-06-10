from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from core.database.favorites import add_to_favorites, remove_from_favorites
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

router = Router()

@router.callback_query(F.data.startswith("addfav_"))
async def handle_add_favorite(callback: types.CallbackQuery, state: FSMContext):
    movie_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)

    success = add_to_favorites(user_id, movie_id)
    await callback.answer(
        get_text("added_to_favorites" if success else "add_to_favorites_error", language)
    )

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
