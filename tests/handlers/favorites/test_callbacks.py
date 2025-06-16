import pytest
from unittest.mock import AsyncMock, patch
from handlers.favorites.callbacks import handle_add_favorite, handle_remove_favorite
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

@pytest.mark.asyncio
@patch("handlers.favorites.callbacks.add_to_favorites", return_value=True)
async def test_handle_add_favorite_success(mock_add):
    callback = AsyncMock()
    callback.data = "addfav_123"
    callback.from_user.id = 1
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await handle_add_favorite(callback, state)

    mock_add.assert_called_once_with(1, 123)
    callback.answer.assert_awaited_with(get_text("added_to_favorites", "en"))

@pytest.mark.asyncio
@patch("handlers.favorites.callbacks.add_to_favorites", return_value=False)
async def test_handle_add_favorite_failure(mock_add):
    callback = AsyncMock()
    callback.data = "addfav_123"
    callback.from_user.id = 1
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await handle_add_favorite(callback, state)

    callback.answer.assert_awaited_with(get_text("add_to_favorites_error", "en"))

@pytest.mark.asyncio
@patch("handlers.favorites.callbacks.remove_from_favorites", return_value=True)
async def test_handle_remove_favorite_success(mock_remove):
    callback = AsyncMock()
    callback.data = "delfav_456"
    callback.from_user.id = 1
    callback.message.delete = AsyncMock()
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await handle_remove_favorite(callback, state)

    mock_remove.assert_called_once_with(1, 456)
    callback.answer.assert_awaited_with(get_text("removed_from_favorites", "en"))
    callback.message.delete.assert_awaited_once()

@pytest.mark.asyncio
@patch("handlers.favorites.callbacks.remove_from_favorites", return_value=False)
async def test_handle_remove_favorite_failure(mock_remove):
    callback = AsyncMock()
    callback.data = "delfav_456"
    callback.from_user.id = 1
    callback.message.delete = AsyncMock()
    state = AsyncMock()
    state.get_data.return_value = {"language": "en"}

    await handle_remove_favorite(callback, state)

    callback.answer.assert_awaited_with(get_text("remove_from_favorites_error", "en"))
    callback.message.delete.assert_not_called()
