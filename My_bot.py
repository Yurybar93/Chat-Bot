import telebot
from telebot import types
import operations_rus
import operations_de
import operations_en
import mysql.connector

dbconfig = {'host': 'localhost',
            'user': 'root',
            'password': '355Aa210@',
            'database': 'movies'}

connection = mysql.connector.connect(**dbconfig)
cursor = connection.cursor()

TOKEN = '7398033193:AAE9iO70cjTBXVRhz9tcOAt7UWmEN4PZJQ4'
bot = telebot.TeleBot(TOKEN)

user_state = {}
user_id = 0
# Тексты сообщений на разных языках
texts = {
    'start': {
        'ru': "Выберите язык / Please choose a language",
        'de': "Wählen Sie eine Sprache / Please choose a language",
        'en': "Please choose a language"
    },
    'menu': {
        'ru': "Выберите действие",
        'de': "Wählen Sie eine Aktion",
        'en': "Choose an action"
    },
    'enter_keyword': {
        'ru': "Введите ключевое слово для поиска:",
        'de': "Geben Sie ein Stichwort für die Suche ein:",
        'en': "Enter a keyword for search:"
    },
    'enter_genre_year': {
        'ru': "Введите жанр и год для поиска в формате 'жанр, год':",
        'de': "Geben Sie das Genre und das Jahr für die Suche im Format 'Genre, Jahr' ein:",
        'en': "Enter the genre and year for search in the format 'genre, year':"
    },
    'close': {
        'ru': "До свидания! Заходите еще!",
        'de': "Auf Wiedersehen! Kommen Sie wieder!",
        'en': "Goodbye! Come back again!"
    }
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user_id
    user_id = message.from_user.id
    print(user_id)
    user_state[user_id] = {'language': None, 'current_action': None}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Русский")
    btn2 = types.KeyboardButton("Deutsch")
    btn3 = types.KeyboardButton("English")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, texts['start']['en'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def callback_lang(call):
    user_id = call.from_user.id
    lang_code = call.data.split('_')[1]
    user_state[user_id]['language'] = lang_code
    # Respond to the user with the selected language or further instructions
    bot.send_message(call.message.chat.id, f"Language set to {lang_code}")


@bot.message_handler(func=lambda message: message.text in ["Русский", "Deutsch", "English"])
def handle_language(message):
    user_id = message.from_user.id
    if message.text == "Русский":
        user_state[user_id]['language'] = 'ru'
    elif message.text == "Deutsch":
        user_state[user_id]['language'] = 'de'
    elif message.text == "English":
        user_state[user_id]['language'] = 'en'
    send_action_menu(message)


def send_action_menu(message):
    user_id = message.from_user.id
    language = user_state[user_id]['language']
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Поиск по ключевому слову" if language == 'ru' else "Suche nach Schlüsselwort" if language == 'de' else "Search by keyword", callback_data='1')
    btn2 = types.InlineKeyboardButton("Поиск по жанрам и году" if language == 'ru' else "Suche nach Genres und Jahr" if language == 'de' else "Search by genres and year", callback_data='2')
    btn3 = types.InlineKeyboardButton("Популярные запросы" if language == 'ru' else "Beliebte Anfragen" if language == 'de' else "Popular queries", callback_data='3')
    btn4 = types.InlineKeyboardButton("Закрыть" if language == 'ru' else "Schließen" if language == 'de' else "Close", callback_data='4')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, texts['menu'][language], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_action(call):
    user_id = call.from_user.id
    user_state[user_id]['current_action'] = int(call.data)
    language = user_state[user_id]['language']
    if user_state[user_id]['current_action'] == 1:
        bot.send_message(call.message.chat.id, texts['enter_keyword'][language])
    elif user_state[user_id]['current_action'] == 2:
        bot.send_message(call.message.chat.id, texts['enter_genre_year'][language])
    elif user_state[user_id]['current_action'] == 3:
        handle_popular_queries(call.message)
    elif user_state[user_id]['current_action'] == 4:
        handle_close_action(call.message)



def handle_close_action(message):
    #user_id = message.from_user.id
    global user_id
    language = user_state[user_id]['language']
    cursor = mysql.connector.connect(**dbconfig) 
    connection = mysql.connector.connect(**dbconfig)
    if language == 'ru':
        operations_rus.close_rus(cursor, connection)
    elif language == 'de':
        operations_de.close_de(cursor, connection)
    elif language == 'en':
        operations_en.close_en(cursor, connection)
    bot.send_message(message.chat.id, texts['close'][language])


@bot.message_handler(func=lambda message: user_state.get(message.from_user.id, {}).get('current_action') in [1, 2])
def handle_keyword_or_genre_year(message):
    user_id = message.from_user.id
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor()
    current_action = user_state[user_id]['current_action']
    language = user_state[user_id]['language']
    result = ''

    if current_action == 1:
        keyword = message.text
        if language == 'ru':
            result = operations_rus.search_by_keyword_rus(cursor, keyword)
        elif language == 'de':
            result = operations_de.search_by_keyword_de(cursor, keyword)
        elif language == 'en':
            result = operations_en.search_by_keyword_en(cursor, keyword)
    elif current_action == 2:
        try:
            genre, year = message.text.split(', ')
            if language == 'ru':
                result = operations_rus.search_by_genres_year_rus(cursor, genre, year)
            elif language == 'de':
                result = operations_de.search_by_genres_year_de(cursor, genre, year)
            elif language == 'en':
                result = operations_en.search_by_genres_year_en(cursor, genre, year)
        except ValueError:
            result = "Ошибка: Введите данные в формате 'жанр, год'." if language == 'ru' else \
                     "Fehler: Geben Sie die Daten im Format 'Genre, Jahr' ein." if language == 'de' else \
                     "Error: Enter the data in the format 'genre, year'."
    
  
    if isinstance(result, str) and len(result) > 4096:
        for i in range(0, len(result), 4096):
            bot.send_message(message.chat.id, result[i:i+4096])
    elif isinstance(result, list):
        result_str = '\n'.join([f'{row[0]} ({row[1]}) - Рейтинг IMDB: {row[2]}' for row in result])
        if len(result_str) > 4096:
            for i in range(0, len(result_str), 4096):
                bot.send_message(message.chat.id, result_str[i:i+4096])
        else:
            bot.send_message(message.chat.id, result_str)
    else:
        bot.send_message(message.chat.id, result)

    cursor.close()
    connection.close()


@bot.message_handler(content_types=['text'])
def handle_popular_queries(message):
    #user_id = message.from_user.id
    global user_id
    print(user_id)
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor()
    language = user_state[user_id]['language']
    result = ''
    
    if language == 'ru':
        result = operations_rus.get_popular_queries(cursor)
    elif language == 'de':
        result = operations_de.get_popular_queries(cursor)
    elif language == 'en':
        result = operations_en.get_popular_queries(cursor)
    
    

  
    if result:
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, "Нет популярных запросов.")

    cursor.close()
    connection.close()


bot.polling(none_stop=True)
