import database

# Function to display the main menu of the application
def menu_en():
    return('''Welcome to the movie search app!

Select an action:
1. Search by keyword
2. Search by genre and year
3. View popular queries
4. Quit the application

Enter an action number: _''')

# Function to search movies by keyword
def search_by_keyword_en(cursor, keyword):
    # SQL query to search for movies using a keyword
    query = '''SELECT title, year, imdb_rating FROM movies
WHERE title LIKE %s OR plot LIKE %s OR genres LIKE %s OR cast LIKE %s OR directors LIKE %s OR year LIKE %s 
ORDER BY imdb_rating DESC'''
    # Save user query for analytics
    database.add_user_query(keyword)
    # Prepare parameters for the SQL query
    param = f'%{keyword}%'
    # Execute the query
    cursor.execute(query, (param, param, param, param, param, param))
    result = cursor.fetchall()
    # Check if any movies are found
    if not result:
        print('No movies found for your keyword.')
    else:
        print('Movies, for your keyword:')
        for row in result:
            print(f'{row[0]}({row[1]})')
    return result

# Function to search movies by genre and year
def search_by_genres_year_en(cursor, genre, year):
    # SQL query to search by genre and year
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
    # Return the result or a message if no matches are found
    if not result:
        return 'No movies according to your parameters were found.'
    else:
        response = 'Movies according to your parameters:'
        for row in result:
            response += f'{row[0]} ({row[1]}) - Rating IMDB: {row[2]}\n'
        return response

# Function to sort the found movies
def sort_en(result):
    print("Select the parameter to sort:")
    print("1. By name")
    print("2. By year")
    print("3. As rated by IMDb")
    
    choice = input("Enter the number of the parameter to be sorted: ")
    # Sorting based on user choice
    if choice == '1':
        sorted_results = sorted(result, key=lambda x: x[0])
    elif choice == '2':
        sorted_results = sorted(result, key=lambda x: x[1])
    elif choice == '3':
        sorted_results = sorted(result, key=lambda x: x[2], reverse=True)
    else:
        print("Incorrect choice.")

    # Printing sorted movies with color indication based on rating
    for row in sorted_results:
        title, year, rating = row
        rating = float(rating)
        if rating > 7.5:
            color = '\033[92m'  # green for ratings above 7.5
        elif 5 <= rating <= 7.5:
            color = '\033[93m'  # yellow for ratings between 5 and 7.5
        else:
            color = '\033[91m'  # red for ratings below 5
        print(f'{color}{title}({year}) {rating}\033[0m')

# Function to get detailed movie information
def get_movie_details_en(cursor):
    title = input('Enter the movie title for more information:')
    # SQL query to get movie details
    query = '''SELECT title, year, genres, plot, imdb_rating, directors, cast FROM movies WHERE title = %s'''
    cursor.execute(query, (title,))
    movie_details = cursor.fetchone()
    
    import re
    # Clean data from extraneous characters
    if movie_details:
        genres = ', '.join(str(genre) for genre in movie_details[2])
        directors = re.sub(r'[$$$$""]', '', movie_details[5])
        cast = re.sub(r'[$$$$""]', '', movie_details[6])
        
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

# Function to close the database connection
def close_en(cursor, connection):
    cursor.close()
    connection.close()
    return 'Goodbye! Come back again!'

# Function to get popular search queries
def get_popular_queries(cursor):
    from datetime import datetime, timedelta
    print("Popular queries for:")
    print("1. Year")
    print("2. Month")
    print("3. All time")
    
    period = int(input())
    # Set the period for fetching popular queries
    if period == 1:
        since_date = datetime.now() - timedelta(days=365)
    elif period == 2:
        since_date = datetime.now() - timedelta(days=30)
    elif period == 3:
        since_date = None
        
    # Fetch popular queries based on the selected period
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
    response = "Popular queries:\n"
    
    # Determine the period for displaying
    if period == 1:
        response = 'Popular queries for one year:\n'
    elif period == 2:
        response = 'Popular queries for one month:\n'
    elif period == 3:
        response = 'Popular queries for all time:\n'
    
    # Check if there are results
    if not result:
        response += "There are no popular requests"
    else:
        # Iterate through the result
        for row in result:
            response += f'{row[0]} - {row[1]} time\n'
    
    print(response)
