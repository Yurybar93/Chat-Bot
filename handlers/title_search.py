from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from utils.texts import get_text
from utils.db import search_movies_by_title, insert_user_query
from handlers.home import get_post_results_keyboard
from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES
from states import SearchByTitle

router = Router()

@router.message(F.text.in_([
    get_text("search_by_title", lang) for lang in AVAILABLE_LANGUAGES
]))
async def start_title_search(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)
    
    await message.answer(get_text("enter_movie_title", language),
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SearchByTitle.waiting_for_title)

@router.message(SearchByTitle.waiting_for_title)
async def finish_title_search(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language", DEFAULT_LANGUAGE)
    title = message.text.strip()

    insert_user_query(title)

    results = search_movies_by_title(title)

    if not results:
        await message.answer(get_text("no_movies_found", language))
    else:
        for title, year, rating in results:
            msg = f"🎬 <b>{title}</b> ({year})\n⭐️ {rating}\n\n📖 /details_{title.replace(' ', '_')}"
            await message.answer(msg, parse_mode="HTML")

    await message.answer(
    get_text("back_to_search_prompt", language),
    reply_markup=get_post_results_keyboard(language)
)

    await state.clear()
    await state.update_data(language=language)