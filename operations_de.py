import database

# Funktion zur Anzeige des Hauptmenüs der Anwendung
def menu_de():
    return('''Willkommen bei der Filmsuch-App!

Wählen Sie eine Aktion:
1. Suche nach Stichwort
2. Suche nach Genre und Jahr der Veröffentlichung
3. Beliebte Suchanfragen anzeigen
4. Beenden Sie die Anwendung

Geben Sie eine Aktionsnummer ein: _''')

# Funktion zur Suche von Filmen nach Stichwort
def search_by_keyword_de(cursor, keyword):
    # SQL-Abfrage zur Suche von Filmen basierend auf einem Stichwort
    query = '''SELECT title, year, imdb_rating FROM movies
WHERE title LIKE %s OR plot LIKE %s OR genres LIKE %s OR cast LIKE %s OR directors LIKE %s OR year LIKE %s 
ORDER BY imdb_rating DESC'''
    # Speichert die Benutzeranfrage für die Analyse
    database.add_user_query(keyword)
    # Vorbereitung der Parameter für die SQL-Abfrage
    param = f'%{keyword}%'
    # Ausführung der Abfrage
    cursor.execute(query, (param, param, param, param, param, param))
    result = cursor.fetchall()
    # Überprüfung, ob Filme gefunden wurden
    if not result:
        print('Es wurden keine Filme für Ihren Suchbegriff gefunden.')
    else:
        print('Filme nach Ihrem Stichwort:')
        for row in result:
            print(f'{row[0]}({row[1]})')
    return result

# Funktion zur Suche nach Filmen nach Genre und Jahr der Veröffentlichung
def search_by_genres_year_de(cursor, genre, year):
    # SQL-Abfrage zur Suche nach Genre und Jahr
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
    # Rückgabe des Ergebnisses oder einer Nachricht, wenn keine Übereinstimmungen gefunden wurden
    if not result:
        return 'Es wurden keine Filme gefunden, die Ihren Parametern entsprechen.'
    else:
        response = 'Filme nach Ihren Parametern:'
        for row in result:
            response += f'{row[0]} ({row[1]}) - Bewertung IMDB: {row[2]}\n'
        return response

# Funktion zum Sortieren der gefundenen Filme
def sort_de(result):
    print("Wählen Sie den zu sortierenden Parameter aus:")
    print("1. Nach Name")
    print("2. Nach Jahr")
    print("3. Wie von IMDb bewertet")
    
    choice = input("Geben Sie die Nummer des zu sortierenden Parameters ein: ")
    # Sortierung basierend auf der Benutzerwahl
    if choice == '1':
        sorted_results = sorted(result, key=lambda x: x[0])
    elif choice == '2':
        sorted_results = sorted(result, key=lambda x: x[1])
    elif choice == '3':
        sorted_results = sorted(result, key=lambda x: x[2], reverse=True)
    else:
        print("Falsche Wahl.")

    # Ausgabe sortierter Filme mit Farbanzeige basierend auf der Bewertung
    for row in sorted_results:
        title, year, rating = row
        rating = float(rating)
        if rating > 7.5:
            color = '\033[92m'  # grün für Bewertungen über 7.5
        elif 5 <= rating <= 7.5:
            color = '\033[93m'  # gelb für Bewertungen zwischen 5 und 7.5
        else:
            color = '\033[91m'  # rot für Bewertungen unter 5
        print(f'{color}{title}({year}) {rating}\033[0m')

# Funktion um detaillierte Informationen zu einem Film zu erhalten
def get_movie_details_de(cursor):
    title = input('Geben Sie den Titel des Films ein, um Einzelheiten zu erfahren:')
    # SQL-Abfrage, um Filmdetails zu erhalten
    query = '''SELECT title, year, genres, plot, imdb_rating, directors, cast FROM movies WHERE title = %s'''
    cursor.execute(query, (title,))
    movie_details = cursor.fetchone()
    
    import re
    # Bereinigung der Daten von überflüssigen Zeichen
    if movie_details:
        genres = ', '.join(str(genre) for genre in movie_details[2])
        directors = re.sub(r'[$$$$""]', '', movie_details[5])
        cast = re.sub(r'[$$$$""]', '', movie_details[6])
        
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

# Funktion zum Schließen der Datenbankverbindung
def close_de(cursor, connection):
    cursor.close()
    connection.close()
    return 'Auf Wiedersehen! Kommen Sie wieder!'

# Funktion um beliebte Suchanfragen zu erhalten
def get_popular_queries(cursor):
    query = """
        SELECT keyword, COUNT(*) as count
        FROM user_queries
        GROUP BY keyword
        ORDER BY count DESC
        LIMIT 5;
        """
    
    cursor.execute(query)
    
    # Abruf aller Ergebnisse
    result = cursor.fetchall()
    
    # Überprüfung, ob das Ergebnis leer ist
    if not result:
        return "Keine populären Anfragen."

    response = 'Beliebte Suchanfragen:\n'
    
    # Iteration durch das Ergebnis
    for row in result:
        response += f'{row[0]} - {row[1]} mal\n'

    return response
``
