# Movie Search Telegram Bot

This project is a multilingual Telegram bot designed to search and analyze movies based on keywords, genres, and release years using a MySQL database. The bot supports English, Russian, and German languages and provides functionality such as keyword search, genre and year search, and popular query retrieval.

## Features

- Multilingual support: English, Russian, and German
- Search for movies by keyword
- Search for movies by genre and release year
- View popular search queries
- Secure database configuration using environment variables

## Prerequisites

- Python 3.7 or later
- MySQL database server
- Telegram account with a bot token from [BotFather](https://core.telegram.org/bots#botfather)

## Setup

### 1. Clone the repository


git clone https://github.com/Yurybar93/Chat-Bot.git
cd Chat-Bot

### 2. Create and Configure the Database
Use the provided database_setup.sql file to set up your database schema. Ensure your MySQL server is running and accessible.

Connect to your MySQL server and execute the SQL file to set up the database schema and tables

### 3. Configure your environment variables for database credentials. This method keeps sensitive information out of your codebase:
```
export DB_HOST='localhost'
export DB_USER='yourusername'
export DB_PASSWORD='yourpassword'
export DB_NAME='movies'
```
### 4. Install Dependencies
Ensure you have all necessary Python packages installed. You can install them with:
```
pip install -r requirements.txt
```
### 5. Set Up the Telegram Bot
Create your bot using the BotFather and obtain a bot token.
Add your token as an environment variable
```
export TELEGRAM_TOKEN='your_bot_token'
```
### 6. Run the Bot
With everything set up, you can now run the bot:
```
python bot.py
```
