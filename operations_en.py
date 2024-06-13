import database
def menu_en():
    return('''Welcome to the movie search app!

Select an action:
1. Search by keyword
2. Search by genre and year
3. View popular queries
4. Quit the application

Enter an action number: _''')
def search_by_keyword_en(cursor, keyword):
    query = '''SELECT title, year, imdb_rating FROM movies
WHERE title LIKE %s OR plot LIKE %s OR genres LIKE %s OR cast LIKE %s OR directors LIKE %s OR year LIKE %s 
ORDER BY imdb_rating DESC'''
    database.add_user_query(keyword)
    param = f'%{keyword}%'
    cursor.execute(query, (param, param, param,param,param,param))
    result = cursor.fetchall()
    if not result:
        print('No movies found for your keyword.')
    else:
        print('Movies, for your keyword:')
        for row in result:
            print(f'{row[0]}({row[1]})')
    return result
 
def search_by_genres_year_en(cursor, genre, year):
    query = '''SELECT title, year, imdb_rating FROM movies
WHERE genres LIKE %s AND year = %s
ORDER BY imdb_rating DESC'''
    genre_param = f'%{genre}%'
    try:
        year = int(year)
    except ValueError:
        return "Error: The year should be a number."
    
    cursor.execute(query, (genre_param, year))
    result = cursor.fetchall()
    if not result:
        return 'No movies according to your parameters were found.'
    else:
        response = 'Movies according to your parameters:'
        for row in result:
            response += f'{row[0]} ({row[1]}) - Rating IMDB: {row[2]}\n'
        return response
def sort_en(result):
    print("Select the parameter to sort:")
    print("1. By name")
    print("2. By year")
    print("3. As rated by IMDb")
    
    choice = input("Enter the number of the parameter to be sorted: ")
    if choice == '1':
        sorted_results = sorted(result, key=lambda x: x[0])
    elif choice == '2':
        sorted_results = sorted(result, key=lambda x: x[1])
    elif choice == '3':
        sorted_results = sorted(result, key=lambda x: x[2], reverse=True)
    else:
        print("Incorrect choice.")
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
def get_movie_details_en(cursor):
    title = input('Enter the movie title for more information:')
    query = '''SELECT title, year, genres, plot, imdb_rating, directors, cast FROM movies WHERE title = %s'''
    cursor.execute(query, (title,))
    movie_details = cursor.fetchone()
    import re
    genres = ', '.join(str(genre) for genre in movie_details[2])
    directors = re.sub(r'[\[\]""]', '', movie_details[5])
    cast = re.sub(r'[\[\]""]', '', movie_details[6])
    if movie_details:
        print("Detailed information about the movie:")
        print(f"Title: {movie_details[0]}")
        print(f"Year: {movie_details[1]}")
        print(f"Genres: {genres}")
        print(f"Plot: {movie_details[3]}")
        print(f"IMDb Rating: {movie_details[4]}")
        print(f"Directors: {directors}")
        print(f"Cast: {cast}")
    else:
        print("The movie was not found.")
def close_en(cursor, connection):
    cursor.close()
    connection.close()
    return 'Goodbye! Come back again!'
def get_popular_queries(cursor):
    from datetime import datetime, timedelta
    print("Popular queries for:")
    print("1. Year")
    print("2. Month")
    print("3. All time")
    period = int(input())
    if period == 1:
        since_date = datetime.now() - timedelta(days=365)
    elif period == 2:
            since_date = datetime.now() - timedelta(days=30)
    elif period == 3:
        since_date = None
    if since_date:
        query = """
            SELECT keyword, COUNT(*) as count
            FROM user_queries
            WHERE search_date >= %s
            GROUP BY keyword
            ORDER BY count DESC
            LIMIT 5;
            """
        cursor.execute(query, (since_date,))
    else:
        query = """
            SELECT keyword, COUNT(*) as count
            FROM user_queries
            GROUP BY keyword
            ORDER BY count DESC
            LIMIT 5;
            """
        cursor.execute(query)

    result = cursor.fetchall()
    if period == 1:
        print('Popular queries for one year:')
    if period == 2:
        print('Popular queries for one month:')
    if period == 3:
        print('Popular queries for all time:')
    for row in result:
            print(f'{row[0]} - {row[1]} time') 
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
        return "There are no popular requests"

    response = 'Popular queries:\n'
    
    # Iterate through the result
    for row in result:
        response += f'{row[0]} - {row[1]} time\n'

   
    return response