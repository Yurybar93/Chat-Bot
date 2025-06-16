import pytest
from unittest.mock import AsyncMock, patch
from aiogram import types
from handlers.menu.main_menu import handle_main_menu_buttons
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

@pytest.mark.asyncio
@patch("handlers.menu.main_menu.get_search_menu")
async def test_handle_find_movie(get_menu):
    message = AsyncMock()
    message.text = get_text("find_movie", "en")
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await handle_main_menu_buttons(message, state)

    message.answer.assert_awaited_with(
        get_text("search_prompt", "en"),
        reply_markup=get_menu.return_value
    )

@pytest.mark.asyncio
@patch("handlers.menu.main_menu.get_user_favorites", return_value=[])
async def test_handle_favorites_empty(mock_fav):
    message = AsyncMock()
    message.text = get_text("favorites", "en")
    message.from_user.id = 1
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await handle_main_menu_buttons(message, state)

    message.answer.assert_awaited_with(get_text("no_favorites", "en"))

@pytest.mark.asyncio
@patch("handlers.menu.main_menu.get_user_favorites")
@patch("handlers.menu.main_menu.format_movie_preview")
async def test_handle_favorites_with_movies(mock_format_preview, mock_get_fav):
    message = AsyncMock()
    message.text = get_text("favorites", "en")
    message.from_user.id = 123
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    mock_get_fav.return_value = [
        (1, "Test Movie", 2020, 8.0)
    ]
    mock_format_preview.return_value = "🎬 Test Movie (2020)\n⭐️ 8.0"

    await handle_main_menu_buttons(message, state)

    assert any("Test Movie" in call.args[0] for call in message.answer.await_args_list), \
        "Expected movie preview text not found in message.answer calls"

    found_button = False
    for call in message.answer.await_args_list:
        markup = call.kwargs.get("reply_markup")
        if isinstance(markup, types.InlineKeyboardMarkup):
            for row in markup.inline_keyboard:
                for btn in row:
                    if btn.callback_data == "delfav_1":
                        found_button = True
                        break

    assert found_button, "Inline button with callback_data 'delfav_1' not found"

@pytest.mark.asyncio
@patch("handlers.menu.main_menu.get_settings_menu")
async def test_handle_settings(get_menu):
    message = AsyncMock()
    message.text = get_text("settings", "en")
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await handle_main_menu_buttons(message, state)

    message.answer.assert_awaited_with(
        get_text("settings_menu", "en"),
        reply_markup=get_menu.return_value
    )
