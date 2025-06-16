from unittest.mock import patch, MagicMock
from core.database.connection import create_connection

@patch("core.database.connection.mysql.connector.connect")
def test_create_connection_success(mock_connect):
    mock_conn = MagicMock()
    mock_conn.is_connected.return_value = True
    mock_connect.return_value = mock_conn

    conn = create_connection()
    assert conn is not None
    mock_connect.assert_called_once()

@patch("core.database.connection.mysql.connector.connect", side_effect=Exception("Connection failed"))
def test_create_connection_failure(mock_connect):
    conn = create_connection()
    assert conn is None
