from core.database.connection import create_connection
from datetime import datetime

def add_to_favorites(user_id: int, movie_id: int):
    conn = create_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO user_favorites (user_id, movie_id, added_at)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE added_at = VALUES(added_at)
        """
        cursor.execute(query, (user_id, movie_id, datetime.now()))
        conn.commit()
        return True
    except Exception as e:
        print(f"DB ERROR (add_to_favorites): {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def remove_from_favorites(user_id: int, movie_id: int):
    conn = create_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM user_favorites WHERE user_id = %s AND movie_id = %s"
        cursor.execute(query, (user_id, movie_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"DB ERROR (remove_from_favorites): {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_favorites(user_id: int):
    conn = create_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = """
        SELECT m.id, m.title, m.year, m.imdb_rating
        FROM movies m
        JOIN user_favorites f ON m.id = f.movie_id
        WHERE f.user_id = %s
        ORDER BY f.added_at DESC
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"DB ERROR (get_user_favorites): {e}")
        return []
    finally:
        cursor.close()
        conn.close()