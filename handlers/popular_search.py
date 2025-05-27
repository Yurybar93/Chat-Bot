from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES
from utils.texts import get_text
from utils.db import get_popular_keywords

router = Router()

@router.message(F.text.in_([
    get_text("search_popular", lang) for lang in AVAILABLE_LANGUAGES
]))
async def handle_popular_searches(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language", DEFAULT_LANGUAGE)
    keywords = get_popular_keywords(5)

    if not keywords:
        await message.answer(get_text("no_popular_queries", language))
    else:
        lines = [f"🔥 <b>{kw}</b> — {count} {get_text('times_searched', language)}" for kw, count in keywords]
        text = f"{get_text("search_popular", language)}\n\n" + "\n".join(lines)
        await message.answer(text, parse_mode="HTML")
