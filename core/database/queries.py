from core.database.connection import create_connection
from datetime import datetime

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
        query = '''
        SELECT keyword, COUNT(*) as count
        FROM user_queries
        GROUP BY keyword
        ORDER BY count DESC
        LIMIT %s
        '''
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        print(f"DB ERROR (popular keywords): {e}")
        return []
