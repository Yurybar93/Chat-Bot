import pytest
from unittest.mock import AsyncMock, patch
from handlers.search.movie_details import show_movie_details
from config import DEFAULT_LANGUAGE
from core.utils.texts import get_text


@pytest.mark.asyncio
@patch("handlers.search.movie_details.get_movie_details_by_title")
async def test_show_movie_details_found(mock_get_details):
    mock_get_details.return_value = (
        1, "Interstellar", 2014, "['Sci-Fi', 'Adventure']", 
        "A journey through space and time", 8.6, 
        "['Christopher Nolan']", "['Matthew McConaughey']"
    )

    message = AsyncMock()
    message.text = "/details_Interstellar"
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await show_movie_details(message, state)

    # Checking that the response contains a title and rating
    sent_text = message.answer.await_args_list[0][0][0]
    assert "Interstellar" in sent_text
    assert "8.6" in sent_text
    assert "Christopher Nolan" in sent_text
    assert "Matthew McConaughey" in sent_text
    assert "Sci-Fi" in sent_text

    # Checking that there is an inline button
    assert message.answer.await_args_list[0][1]["reply_markup"] is not None


@pytest.mark.asyncio
@patch("handlers.search.movie_details.get_movie_details_by_title", return_value=None)
async def test_show_movie_details_not_found(mock_get_details):
    message = AsyncMock()
    message.text = "/details_UnknownMovie"
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await show_movie_details(message, state)

    message.answer.assert_awaited_with(get_text("movie_not_found", DEFAULT_LANGUAGE))


@pytest.mark.asyncio
async def test_show_movie_details_invalid_command():
    message = AsyncMock()
    message.text = "/detailz_NoMatch"  # Invalid command that doesn't match the expected pattern
    state = AsyncMock()

    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await show_movie_details(message, state)

    message.answer.assert_not_awaited()
