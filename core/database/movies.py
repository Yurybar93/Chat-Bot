from core.database.connection import create_connection
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

def search_movies_by_title(title: str, limit: int = 10) -> list[tuple[str, int, int]]:
    connection = create_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        query = """
        SELECT title, year, imdb_rating
        FROM movies
        WHERE LOWER(title) LIKE LOWER(%s)
        ORDER BY imdb_rating DESC
        LIMIT %s
        """
        like_pattern = f"%{title}%"
        cursor.execute(query, (like_pattern, limit))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Error as e:
        print(f"DB ERROR: {e}")
        return []
    
def search_movies_by_keyword(keyword: str, limit: int = 10):
    connection = create_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        like_pattern = f"%{keyword}%"
        query = '''
            SELECT title, year, imdb_rating 
            FROM movies
            WHERE 
                title LIKE %s OR
                plot LIKE %s OR
                genres LIKE %s OR
                cast LIKE %s OR
                directors LIKE %s OR
                year LIKE %s
            ORDER BY imdb_rating DESC
            LIMIT %s
        '''
        params = (like_pattern,) * 6 + (limit,)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        print(f"DB ERROR (keyword search): {e}")
        return []

def get_movie_details_by_title(title: str):
    connection = create_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        query = '''
            SELECT id, title, year, genres, plot, imdb_rating, directors, cast
            FROM movies
            WHERE title = %s
        '''
        cursor.execute(query, (title,))
        return cursor.fetchone()

    except Exception as e:
        print(f"DB ERROR (movie details): {e}")
        return None
    finally:
        cursor.close()
        connection.close()