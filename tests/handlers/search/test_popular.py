import pytest
from unittest.mock import AsyncMock, patch
from handlers.search.popular import handle_popular_searches
from core.utils.texts import get_text
from config import DEFAULT_LANGUAGE

@pytest.mark.asyncio
@patch("handlers.search.popular.get_popular_keywords", return_value=[])
async def test_handle_popular_searches_empty(mock_get_keywords):
    # Arrange
    message = AsyncMock()
    message.text = get_text("search_popular", DEFAULT_LANGUAGE)
    message.answer = AsyncMock()

    state = AsyncMock()
    state.get_data = AsyncMock(return_value={"language": DEFAULT_LANGUAGE})

    # Act
    await handle_popular_searches(message, state)

    # Assert
    message.answer.assert_awaited_once_with(get_text("no_popular_queries", DEFAULT_LANGUAGE))


@pytest.mark.asyncio
@patch("handlers.search.popular.get_popular_keywords", return_value=[("avatar", 3), ("matrix", 2)])
async def test_handle_popular_searches_with_keywords(mock_get_keywords):
    # Arrange
    message = AsyncMock()
    message.text = get_text("search_popular", DEFAULT_LANGUAGE)
    message.answer = AsyncMock()

    state = AsyncMock()
    state.get_data = AsyncMock(return_value={"language": DEFAULT_LANGUAGE})

    # Act
    await handle_popular_searches(message, state)

    # Assert
    assert message.answer.await_args.kwargs["parse_mode"] == "HTML"
    called_text = message.answer.await_args.args[0]
    assert "🔥 <b>avatar</b> — 3" in called_text
    assert "🔥 <b>matrix</b> — 2" in called_text
    assert get_text("search_popular", DEFAULT_LANGUAGE) in called_text
