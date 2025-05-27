from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils.texts import get_text
from utils.db import get_movies_by_genre_and_year
from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES
from utils.genre_map import GENRE_TRANSLATIONS

router = Router()

class SearchGenreYear(StatesGroup):
    choosing_genre = State()
    choosing_year = State()

def get_localized_genres(language: str) -> list[str]:
    return [v[language] for v in GENRE_TRANSLATIONS.values()]

def get_english_genre(localized: str, user_lang: str) -> str:
    for eng, langs in GENRE_TRANSLATIONS.items():
        if langs.get(user_lang) == localized:
            return eng
    return localized

@router.message(F.text.in_([
    get_text("search_by_genre_year", lang) for lang in AVAILABLE_LANGUAGES
]))
async def start_genre_search(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)
    genres = get_localized_genres(language)
    buttons = [[types.KeyboardButton(text=genre)] for genre in genres]

    await message.answer(get_text("choose_genre", language),
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))
    await state.set_state(SearchGenreYear.choosing_genre)

@router.message(SearchGenreYear.choosing_genre)
async def get_year_input(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language", DEFAULT_LANGUAGE)
    english_genre = get_english_genre(message.text, language)
    await state.update_data(selected_genre=english_genre)

    await message.answer(get_text("enter_year", language),
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SearchGenreYear.choosing_year)

@router.message(SearchGenreYear.choosing_year)
async def finish_search(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", DEFAULT_LANGUAGE)
    genre = data.get("selected_genre")  # уже на английском
    year = message.text.strip()

    if not year.isdigit() or not (1900 <= int(year) <= 2100):
        await message.answer(get_text("invalid_year", language))
        return

    await message.answer(get_text("searching", language))

    movies = get_movies_by_genre_and_year(genre, int(year))

    if not movies:
        await message.answer(get_text("no_movies_found", language))
    else:
        for title, year, rating in movies:
            msg = f"🎬 <b>{title}</b> ({year})\n⭐️ {rating}"
            await message.answer(msg, parse_mode="HTML")

    await state.clear()
