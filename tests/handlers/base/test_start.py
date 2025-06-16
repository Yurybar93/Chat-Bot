import pytest
from unittest.mock import AsyncMock, patch
from handlers.base.start import start_command
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

@pytest.mark.asyncio
@patch("handlers.base.start.get_language_keyboard")
async def test_start_command(mock_get_keyboard):
    message = AsyncMock()
    message.from_user.id = 12345
    state = AsyncMock()

    mock_keyboard = AsyncMock()
    mock_get_keyboard.return_value = mock_keyboard

    await start_command(message, state)

    # Assert that the FSM state was cleared
    state.clear.assert_awaited_once()

    # Assert that the correct start message was sent
    expected_text = get_text("start_message", DEFAULT_LANGUAGE)
    message.answer.assert_awaited_with(expected_text, reply_markup=mock_keyboard)

    # Assert that the language keyboard was generated
    mock_get_keyboard.assert_called_once()
