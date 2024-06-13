import database

def menu_de():
    return('''Willkommen bei der Filmsuch-App!

Wählen Sie eine Aktion:
1. Suche nach Stichwort
2. Suche nach Genre und Jahr der Veröffentlichung
3. Beliebte Suchanfragen anzeigen
4. Beenden Sie die Anwendung

Geben Sie eine Aktionsnummer ein: _''')
def search_by_keyword_de(cursor, keyword):
    query = '''SELECT title, year, imdb_rating FROM movies
WHERE title LIKE %s OR plot LIKE %s OR genres LIKE %s OR cast LIKE %s OR directors LIKE %s OR year LIKE %s 
ORDER BY imdb_rating DESC'''
    database.add_user_query(keyword)
    param = f'%{keyword}%'
    cursor.execute(query, (param, param, param,param,param,param))
    result = cursor.fetchall()
    if not result:
        print('Es wurden keine Filme für Ihren Suchbegriff gefunden.')
    else:
        print('Filme nach Ihrem Stichwort')
        for row in result:
            print(f'{row[0]}({row[1]})')
    return result
def search_by_genres_year_de(cursor, genre, year):
    query = '''SELECT title, year, imdb_rating FROM movies
WHERE genres LIKE %s AND year = %s
ORDER BY imdb_rating DESC'''
    genre_param = f'%{genre}%'
    try:
        year = int(year)
    except ValueError:
        return "Fehler: Das Jahr sollte eine Zahl sein."
    
    cursor.execute(query, (genre_param, year))
    result = cursor.fetchall()
    if not result:
        return 'Es wurden keine Filme gefunden, die Ihren Parametern entsprechen.'
    else:
        response = 'Filme nach Ihren Parametern:'
        for row in result:
            response += f'{row[0]} ({row[1]}) - Bewertung IMDB: {row[2]}\n'
        return response
def sort_de(result):
    print("Wählen Sie den zu sortierenden Parameter aus:")
    print("1. Nach Name")
    print("2. Nach Jahr")
    print("3. Wie von IMDb bewertet")
    
    choice = input("Geben Sie die Nummer des zu sortierenden Parameters ein: ")
    if choice == '1':
        sorted_results = sorted(result, key=lambda x: x[0])
    elif choice == '2':
        sorted_results = sorted(result, key=lambda x: x[1])
    elif choice == '3':
        sorted_results = sorted(result, key=lambda x: x[2], reverse=True)
    else:
        print("Falsche Wahl.")
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
def get_movie_details_de(cursor):
    title = input('Geben Sie den Titel des Films ein, um Einzelheiten zu erfahren:')
    query = '''SELECT title, year, genres, plot, imdb_rating, directors, cast FROM movies WHERE title = %s'''
    cursor.execute(query, (title,))
    movie_details = cursor.fetchone()
    import re
    genres = ', '.join(str(genre) for genre in movie_details[2])
    directors = re.sub(r'[\[\]""]', '', movie_details[5])
    cast = re.sub(r'[\[\]""]', '', movie_details[6])
    if movie_details:
        print("Weitere Informationen über den Film:")
        print(f"Titel: {movie_details[0]}")
        print(f"Jahr: {movie_details[1]}")
        print(f"Genres: {genres}")
        print(f"Handlung: {movie_details[3]}")
        print(f"Bewertung IMDb: {movie_details[4]}")
        print(f"Direktoren: {directors}")
        print(f"Schauspieler: {cast}")
    else:
        print("Film nicht gefunden.")
def close_de(cursor, connection):
    cursor.close()
    connection.close()
    return 'Auf Wiedersehen! Kommen Sie wieder!'
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
        return "Keine populären Anfragen."

    response = 'Beliebte Suchanfragen:\n'
    
    # Iterate through the result
    for row in result:
        response += f'{row[0]} - {row[1]} mal\n'

   
    return response