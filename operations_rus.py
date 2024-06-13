import database

def menu_rus():
    return('''Добро пожаловать в приложение по поиску фильмов!

Выберите действие:
1. Поиск по ключевому слову
2. Поиск по жанру и году выпуска
3. Просмотр популярных запросов
4. Выйти из приложения

Введите номер действия: _''')  
def search_by_keyword_rus(cursor, keyword):
    query = '''SELECT title, year, imdb_rating FROM movies
WHERE title LIKE %s OR plot LIKE %s OR genres LIKE %s OR cast LIKE %s OR directors LIKE %s OR year LIKE %s 
ORDER BY imdb_rating DESC'''
    database.add_user_query(keyword)
    param = f'%{keyword}%'

    cursor.execute(query, (param, param, param, param, param, param))
    result = cursor.fetchall()
    if not result:
        return 'Фильмы, найденные по вашему ключевому слову, не найдены.'
    else:
        return result
def search_by_genres_year_rus(cursor, genre, year):
    query = '''SELECT title, year, imdb_rating FROM movies
WHERE genres LIKE %s AND year = %s
ORDER BY imdb_rating DESC'''
    genre_param = f'%{genre}%'
    try:
        year = int(year)
    except ValueError:
        return "Ошибка: Год должен быть числом."
    
    cursor.execute(query, (genre_param, year))
    result = cursor.fetchall()
    if not result:
        return 'Фильмы по вашим параметрам не найдены.'
    else:
        response = 'Фильмы по вашим параметрам:\n'
        for row in result:
            response += f'{row[0]} ({row[1]}) - Рейтинг IMDB: {row[2]}\n'
        return response
def sort_rus(result):
    print("Выберите параметр для сортировки:")
    print("1. По названию")
    print("2. По году")
    print("3. По рейтингу IMDb")
    
    choice = input("Введите номер параметра для сортировки: ")
    
    if choice == '1':
        sorted_results = sorted(result, key=lambda x: x[0])
    elif choice == '2':
        sorted_results = sorted(result, key=lambda x: x[1])
    elif choice == '3':
        sorted_results = sorted(result, key=lambda x: x[2], reverse=True)
    else:
        print("Некорректный выбор.")
        return
    
    for row in sorted_results:
        title, year, rating = row
        rating = float(rating)
        if rating > 7.5:
            color = '\033[92m' 
        elif 5 <= rating <= 7.5:
            color = '\033[93m' 
        else:
            color = '\033[91m'  
        print(f'{color}{title}({year}) {rating}\033[0m')
        
       
def get_movie_details(cursor):
    title = input('Введите название фильма для получения подробной информации:')
    query = '''SELECT title, year, genres, plot, imdb_rating, directors, cast FROM movies WHERE title = %s'''
    cursor.execute(query, (title,))
    movie_details = cursor.fetchone()
    import re
    genres = ', '.join(str(genre) for genre in movie_details[2])
    directors = re.sub(r'[\[\]""]', '', movie_details[5])
    cast = re.sub(r'[\[\]""]', '', movie_details[6])
    if movie_details:
        print("Подробная информация о фильме:")
        print(f"Название: {movie_details[0]}")
        print(f"Год: {movie_details[1]}")
        print(f"Жанры: {genres}")
        print(f"Сюжет: {movie_details[3]}")
        print(f"Рейтинг IMDb: {movie_details[4]}")
        print(f"Режиссеры: {directors}")
        print(f"Актерский состав: {cast}")
    else:
        print("Фильм не найден.")
def close_rus(cursor, connection):
    cursor.close()
    connection.close()
    response = 'До свидания! Заходите еще!'
    return response

def get_popular_queries(cursor):
    query = """
        SELECT keyword, COUNT(*) as count
        FROM user_queries
        GROUP BY keyword
        ORDER BY count DESC
        LIMIT 5;
        """
    
    cursor.execute(query)
    
    # Fetch all results
    result = cursor.fetchall()
    

    # Check if result is empty
    if not result:
        print("DEBUG: Нет результатов")
        return "Нет популярных запросов."

    response = 'Самые популярные запросы за все время:\n'
    
    # Iterate through the result
    for row in result:
        response += f'{row[0]} - {row[1]} раз(а)\n'

   
    return response
