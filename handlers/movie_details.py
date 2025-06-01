from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from utils.db import get_movie_details_by_title
from utils.texts import get_text
from config import DEFAULT_LANGUAGE
from aiogram.fsm.context import FSMContext
import ast

router = Router()

@router.message(F.text.regexp(r"^/details_(.+)"))
async def show_movie_details(message: types.Message, state: FSMContext):

    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)
    print(f"[DEBUG] Detected language: {language}")
    print(get_text("movie_details_format", language))

    match = re.match(r"^/details_(.+)", message.text)
    if not match:
        return

    raw_title = match.group(1)
    title = raw_title.replace("_", " ")

    details = get_movie_details_by_title(title)

    if not details:
        await message.answer(get_text("movie_not_found", language))
        return

    movie_id, title, year, genres, plot, rating, directors, cast = details

    def clean(value):
    # если значение уже список/множество/кортеж — просто склеиваем
        if isinstance(value, (list, set, tuple)):
            return ", ".join(str(v) for v in value)

    # если это строка — пробуем распарсить
        if isinstance(value, str):
            try:
                parsed = ast.literal_eval(value)
                if isinstance(parsed, (list, set, tuple)):
                    return ", ".join(str(v) for v in parsed)
            except Exception:
            # если не удалось распарсить — удалим скобки вручную
                cleaned = value.strip("{}[]()").replace("'", "").replace('"', '')
                return ", ".join(part.strip() for part in cleaned.split(","))
    
        return str(value)

    msg = get_text("movie_details_format", language).format(
        title=title,
        year=year,
        genres=clean(genres),
        directors=clean(directors),
        cast=clean(cast),
        rating=rating,
        plot=plot
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Add to favorites", callback_data=f"addfav_{movie_id}")]
    ])

    await message.answer(msg, parse_mode="HTML", reply_markup=keyboard)

