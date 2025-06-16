from unittest.mock import patch, MagicMock
from core.database.movies import (
    get_movies_by_genre_and_year,
    search_movies_by_title,
    search_movies_by_keyword,
    get_movie_details_by_title
)

@patch("core.database.movies.create_connection")
def test_get_movies_by_genre_and_year(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("The Matrix", 1999, 8.7)
    ]

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    result = get_movies_by_genre_and_year("Action", 1999)
    assert isinstance(result, list)
    assert result[0][0] == "The Matrix"

@patch("core.database.movies.create_connection")
def test_search_movies_by_title(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("Interstellar", 2014, 8.6)
    ]

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    result = search_movies_by_title("inter")
    assert len(result) == 1
    assert result[0][0] == "Interstellar"

@patch("core.database.movies.create_connection")
def test_search_movies_by_keyword(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("Inception", 2010, 8.8)
    ]

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    result = search_movies_by_keyword("dream")
    assert result[0][0] == "Inception"

@patch("core.database.movies.create_connection")
def test_get_movie_details_by_title(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (
        42, "Inception", 2010, "Action,Sci-Fi", "A dream inside a dream",
        8.8, "Christopher Nolan", "Leonardo DiCaprio"
    )

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    result = get_movie_details_by_title("Inception")
    assert result is not None
    assert result[1] == "Inception"
