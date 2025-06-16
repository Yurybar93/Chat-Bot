import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import ReplyKeyboardRemove
from config import DEFAULT_LANGUAGE
from core.utils.texts import get_text
from handlers.search.title import start_title_search, finish_title_search
from states.search_states import SearchByTitle


@pytest.mark.asyncio
async def test_start_title_search():
    message = AsyncMock()
    message.answer = AsyncMock()
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await start_title_search(message, state)

    message.answer.assert_called_once_with(
        get_text("enter_movie_title", DEFAULT_LANGUAGE),
        reply_markup=ReplyKeyboardRemove()
    )
    state.set_state.assert_awaited_once_with(SearchByTitle.waiting_for_title)


@pytest.mark.asyncio
@patch("handlers.search.title.search_movies_by_title", return_value=[])
@patch("handlers.search.title.insert_user_query")
@patch("handlers.search.title.get_post_results_keyboard", return_value=AsyncMock())
async def test_finish_title_search_no_results(mock_keyboard, mock_insert, mock_search):
    message = AsyncMock()
    message.text = "Some Movie"
    message.answer = AsyncMock()
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await finish_title_search(message, state)

    mock_insert.assert_called_once_with("Some Movie")
    mock_search.assert_called_once_with("Some Movie")
    message.answer.assert_any_call(get_text("no_movies_found", DEFAULT_LANGUAGE))
    message.answer.assert_awaited()
    state.clear.assert_awaited()
    state.update_data.assert_awaited_with(language=DEFAULT_LANGUAGE)


@pytest.mark.asyncio
@patch("handlers.search.title.search_movies_by_title", return_value=[
    ("The Matrix", 1999, 8.7),
    ("Inception", 2010, 8.8)
])
@patch("handlers.search.title.insert_user_query")
@patch("handlers.search.title.get_post_results_keyboard", return_value=AsyncMock())
@patch("handlers.search.title.format_movie_preview", side_effect=lambda t, y, r: f"{t} ({y}) - {r}")
async def test_finish_title_search_with_results(mock_format, mock_keyboard, mock_insert, mock_search):
    message = AsyncMock()
    message.text = "Sci-fi"
    message.answer = AsyncMock()
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await finish_title_search(message, state)

    assert mock_insert.called
    assert mock_search.called
    assert message.answer.call_count >= 3  # 2 movies + 1 back prompt

    message.answer.assert_any_call("The Matrix (1999) - 8.7", parse_mode="HTML")
    message.answer.assert_any_call("Inception (2010) - 8.8", parse_mode="HTML")

    state.clear.assert_awaited()
    state.update_data.assert_awaited_with(language=DEFAULT_LANGUAGE)
