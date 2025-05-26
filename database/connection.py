import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from utils.logger import logger


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            logger.info("✅ Erfolgreiche Verbindung zur Datenbank!")
            return connection
    except Error as e:
        logger.error(f"❌ Fehler bei der Verbindung zur Datenbank: {e}")
        return None
