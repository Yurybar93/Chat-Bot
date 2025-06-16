import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from core.utils.logger import logger


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
            logger.info("Successful connection to the database!")
            return connection
    except (Error, Exception) as e: 
        logger.error(f"Error connecting to the database: {e}")
        return None
