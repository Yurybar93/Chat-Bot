import pytest
from unittest.mock import AsyncMock
from handlers.menu.settings_menu import handle_change_language
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

@pytest.mark.asyncio
async def test_handle_change_language():
    message = AsyncMock()
    message.text = get_text("change_language", DEFAULT_LANGUAGE)
    state = AsyncMock()
    state.get_data.return_value = {"language": DEFAULT_LANGUAGE}

    await handle_change_language(message, state)

    # Checking that the reply has been sent
    message.answer.assert_awaited()
    call_args = message.answer.call_args

    # Checking the text
    assert get_text("choose_language", DEFAULT_LANGUAGE) in call_args.args[0]

    # Checking that a keyboard is passed
    assert "reply_markup" in call_args.kwargs
