import asyncio
from loader import dp, bot
from utils.logger import logger
from handlers import start, actions, menu, search_menu, setting_menu, genre_search, title_search, popular_search, keyword_search, movie_details, favorites
# from database import favorites

async def main():
    try:
        logger.info("Starting bot...")
        dp.include_router(genre_search.router)
        dp.include_router(title_search.router)
        dp.include_router(popular_search.router)
        dp.include_router(keyword_search.router)
        dp.include_router(movie_details.router)
        dp.include_router(favorites.router)
        dp.include_router(menu.router)
        dp.include_router(search_menu.router)
        dp.include_router(setting_menu.router)
        dp.include_router(start.router)
        dp.include_router(actions.router)
        await dp.start_polling(bot)

    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await bot.close()
        await dp.storage.close()
        await dp.storage.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
