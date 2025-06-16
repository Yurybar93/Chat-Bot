import pytest
from unittest.mock import AsyncMock, patch
from aiogram import types
from handlers.favorites.messages import show_favorites
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

@pytest.mark.asyncio
@patch("handlers.favorites.messages.get_user_favorites", return_value=[])
async def test_show_favorites_empty(mock_get_fav):
    message = AsyncMock()
    message.from_user.id = 123
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await show_favorites(message, state)

    message.answer.assert_awaited_once_with(get_text("no_favorites", "en"))

@pytest.mark.asyncio
@patch("handlers.favorites.messages.get_user_favorites")
@patch("handlers.favorites.messages.format_movie_preview")
async def test_show_favorites_with_movies(mock_format, mock_get_fav):
    message = AsyncMock()
    message.from_user.id = 123
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    mock_get_fav.return_value = [
        (1, "Movie One", 2020, 8.5),
        (2, "Movie Two", 2021, 7.9)
    ]
    mock_format.side_effect = lambda title, year, rating: f"{title} ({year}) ★ {rating}"

    await show_favorites(message, state)

    assert message.answer.await_count == 2

    calls = [call.args[0] for call in message.answer.await_args_list]
    assert "Movie One (2020)" in calls[0]
    assert "Movie Two (2021)" in calls[1]

    # Optional: check if buttons contain correct callback_data
    for call in message.answer.await_args_list:
        markup = call.kwargs["reply_markup"]
        assert isinstance(markup, types.InlineKeyboardMarkup)
        assert markup.inline_keyboard[0][0].callback_data.startswith("delfav_")
