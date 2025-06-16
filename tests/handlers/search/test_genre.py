import pytest
from unittest.mock import AsyncMock, patch
from aiogram.fsm.context import FSMContext
from handlers.search.genre import start_genre_search, get_year_input, finish_search
from states.search_states import SearchGenreYear
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE


@pytest.mark.asyncio
async def test_start_genre_search_sets_state_and_shows_genres():
    message = AsyncMock()
    message.text = get_text("search_by_genre_year", DEFAULT_LANGUAGE)
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await start_genre_search(message, state)

    message.answer.assert_awaited()
    assert get_text("choose_genre", DEFAULT_LANGUAGE) in message.answer.call_args.args[0]
    state.set_state.assert_called_once_with(SearchGenreYear.choosing_genre)


@pytest.mark.asyncio
async def test_get_year_input_sets_genre_and_asks_year():
    message = AsyncMock()
    message.text = "Action"  
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await get_year_input(message, state)

    message.answer.assert_awaited()
    assert get_text("enter_year", DEFAULT_LANGUAGE) in message.answer.call_args.args[0]
    state.set_state.assert_called_once_with(SearchGenreYear.choosing_year)
    state.update_data.assert_awaited()


@pytest.mark.asyncio
async def test_finish_search_invalid_year():
    message = AsyncMock()
    message.text = "abc"
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE, "selected_genre": "Action"}

    await finish_search(message, state)

    message.answer.assert_awaited_with(get_text("invalid_year", DEFAULT_LANGUAGE))


@pytest.mark.asyncio
@patch("handlers.search.genre.get_movies_by_genre_and_year")
async def test_finish_search_valid_results(mock_get_movies):
    mock_get_movies.return_value = [("Movie", 2020, 8.5)]

    message = AsyncMock()
    message.text = "2020"
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE, "selected_genre": "Action"}

    await finish_search(message, state)

    # g if the confirmation text is available
    assert any(get_text("searching_by_genre_year", DEFAULT_LANGUAGE).split("{")[0] in call.args[0]
               for call in message.answer.await_args_list)

    # Checking that there is a movie response
    found_movie = any("Movie" in call.args[0] for call in message.answer.await_args_list)
    assert found_movie

    # Checking that the FSM is cleared
    state.clear.assert_awaited_once()
