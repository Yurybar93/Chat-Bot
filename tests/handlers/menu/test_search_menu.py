import pytest
from unittest.mock import AsyncMock
from handlers.menu.search_menu import handle_back_to_main_menu, back_to_search_menu
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

@pytest.mark.asyncio
async def test_handle_back_to_main_menu():
    message = AsyncMock()
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await handle_back_to_main_menu(message, state)

    # Check the sent message contains correct prompt
    message.answer.assert_awaited()
    assert get_text("back_to_main_menu_prompt", DEFAULT_LANGUAGE) in message.answer.call_args.args[0]

    # Check a keyboard is passed
    assert "reply_markup" in message.answer.call_args.kwargs

@pytest.mark.asyncio
async def test_back_to_search_menu():
    message = AsyncMock()
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await back_to_search_menu(message, state)

    # Check the search prompt is sent
    message.answer.assert_awaited()
    assert get_text("search_prompt", DEFAULT_LANGUAGE) in message.answer.call_args.args[0]

    # Check reply_markup is passed
    assert "reply_markup" in message.answer.call_args.kwargs
