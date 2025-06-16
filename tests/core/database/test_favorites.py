from unittest.mock import patch, MagicMock
from core.database.favorites import (
    add_to_favorites,
    remove_from_favorites,
    get_user_favorites
)

@patch("core.database.favorites.create_connection")
def test_add_to_favorites_success(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    result = add_to_favorites(user_id=1, movie_id=42)

    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("core.database.favorites.create_connection", return_value=None)
def test_add_to_favorites_no_connection(mock_connect):
    result = add_to_favorites(user_id=1, movie_id=42)
    assert result is False

@patch("core.database.favorites.create_connection")
def test_remove_from_favorites_success(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    result = remove_from_favorites(user_id=1, movie_id=42)

    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

@patch("core.database.favorites.create_connection")
def test_get_user_favorites_returns_data(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (42, "Inception", 2010, 8.8)
    ]

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    result = get_user_favorites(user_id=1)

    assert isinstance(result, list)
    assert result[0][1] == "Inception"
