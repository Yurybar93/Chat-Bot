from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from core.utils.texts import get_text
from core.database.movies import search_movies_by_keyword
from core.database.queries import insert_user_query
from core.utils.keyboards import get_post_results_keyboard
from core.services.search_service import format_movie_preview
from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES
from states.search_states import SearchByKeyword

router = Router()
@router.message(F.text.in_([
    get_text("search_by_keyword", lang) for lang in AVAILABLE_LANGUAGES
]))
async def start_keyword_search(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)
    
    await message.answer(get_text("enter_keyword", language),
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SearchByKeyword.waiting_for_keyword)

@router.message(SearchByKeyword.waiting_for_keyword)
async def finish_keyword_search(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language", DEFAULT_LANGUAGE)
    keyword = message.text.strip()

    insert_user_query(keyword)
    
    results = search_movies_by_keyword(keyword)

    if not results:
        await message.answer(get_text("no_movies_found", language))
    else:
        for title, year, rating in results:
            msg = format_movie_preview(title, year, rating)
            await message.answer(msg, parse_mode="HTML")

    await message.answer(
    get_text("back_to_search_prompt", language),
    reply_markup=get_post_results_keyboard(language)
)

    await state.clear()
    await state.update_data(language=language)

