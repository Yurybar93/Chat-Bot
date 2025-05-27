from database.connection import create_connection
from mysql.connector import Error
from datetime import datetime

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


def insert_user_query(keyword: str):
    connection = create_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        search_date = datetime.now()
        query = "INSERT INTO user_queries (keyword, search_date) VALUES (%s, %s)"
        cursor.execute(query, (keyword, search_date))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"DB ERROR (insert_user_query): {e}")
        return False

def get_popular_keywords(limit: int = 5):
    connection = create_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        query = """
        SELECT keyword, COUNT(*) as count
        FROM user_queries
        GROUP BY keyword
        ORDER BY count DESC
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results  # [("Inception", 12), ("Matrix", 8), ...]
    except Exception as e:
        print(f"DB ERROR (popular keywords): {e}")
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
            SELECT title, year, genres, plot, imdb_rating, directors, cast
            FROM movies
            WHERE title = %s
        '''
        cursor.execute(query, (title,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result  
    except Exception as e:
        print(f"DB ERROR (movie details): {e}")
        return None
