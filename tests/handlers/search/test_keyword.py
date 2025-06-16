import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import ReplyKeyboardRemove
from handlers.search.keyword import start_keyword_search, finish_keyword_search
from states.search_states import SearchByKeyword
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE


@pytest.mark.asyncio
async def test_start_keyword_search():
    message = AsyncMock()
    message.text = get_text("search_by_keyword", DEFAULT_LANGUAGE)
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await start_keyword_search(message, state)

    message.answer.assert_awaited_once_with(
        get_text("enter_keyword", DEFAULT_LANGUAGE),
        reply_markup=ReplyKeyboardRemove()  
    )
    state.set_state.assert_called_once_with(SearchByKeyword.waiting_for_keyword)


@pytest.mark.asyncio
@patch("handlers.search.keyword.insert_user_query")
@patch("handlers.search.keyword.search_movies_by_keyword")
async def test_finish_keyword_search_with_results(mock_search, mock_insert):
    mock_search.return_value = [("Interstellar", 2014, 8.6)]

    message = AsyncMock()
    message.text = "space"
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await finish_keyword_search(message, state)

    # Checking the insert_user_query call
    mock_insert.assert_called_once_with("space")

    # Checking that a movie message has been sent
    movie_found = any("Interstellar" in call.args[0] for call in message.answer.await_args_list)
    assert movie_found

    # Checking that the status has been reset
    state.clear.assert_awaited_once()


@pytest.mark.asyncio
@patch("handlers.search.keyword.insert_user_query")
@patch("handlers.search.keyword.search_movies_by_keyword")
async def test_finish_keyword_search_no_results(mock_search, mock_insert):
    mock_search.return_value = []

    message = AsyncMock()
    message.text = "unknownword"
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await finish_keyword_search(message, state)

    message.answer.assert_any_await(get_text("no_movies_found", DEFAULT_LANGUAGE))
    state.clear.assert_awaited_once()
