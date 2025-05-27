from database.connection import create_connection
from mysql.connector import Error

def get_movies_by_genre_and_year(genre: str, year: int, limit: int = 10) -> list[tuple[str, int, int]]:
    connection = create_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        query = """
        SELECT title, year, imdb_rating 
        FROM movies
        WHERE LOWER(genres) LIKE LOWER(%s) AND year = %s
        ORDER BY imdb_rating DESC
        LIMIT %s
        """
        like_pattern = f"%{genre}%"
        cursor.execute(query, (like_pattern, year, limit))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Error as e:
        print(f"DB ERROR: {e}")
        return []
