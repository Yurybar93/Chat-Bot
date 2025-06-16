import pytest
from unittest.mock import AsyncMock
from unittest.mock import AsyncMock, ANY
from handlers.base.actions import set_language, LANGUAGES
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

@pytest.mark.asyncio
async def test_set_supported_language():
    message = AsyncMock()
    state = AsyncMock()
    message.text = LANGUAGES["de"]
    message.from_user.id = 123

    await set_language(message, state)

    state.update_data.assert_awaited_with(language="de")
    message.answer.assert_any_await(get_text("language_set", "de"))
    message.answer.assert_any_await(get_text("welcome_message", "de"), reply_markup=ANY)

@pytest.mark.asyncio
async def test_set_unsupported_language():
    message = AsyncMock()
    state = AsyncMock()

    message.text = "Français"  # Not in LANGUAGES
    message.from_user.id = 1

    await set_language(message, state)

    # Should send error message
    message.answer.assert_awaited_with(get_text("language_not_supported", DEFAULT_LANGUAGE))
