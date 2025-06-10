import asyncio
from core.loader import dp, bot
from core.utils.logger import logger
from handlers.base import start, actions
from handlers.menu import main_menu, search_menu, settings_menu
from handlers.search import genre, title, keyword, popular, movie_details
from handlers.favorites import callbacks, messages 

async def main():
    try:
        logger.info("Starting bot...")
        dp.include_router(genre.router)
        dp.include_router(title.router)
        dp.include_router(keyword.router)
        dp.include_router(popular.router)
        dp.include_router(movie_details.router)
        dp.include_router(callbacks.router)
        dp.include_router(messages.router)
        dp.include_router(main_menu.router)
        dp.include_router(search_menu.router)
        dp.include_router(settings_menu.router)
        dp.include_router(start.router)
        dp.include_router(actions.router)
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user.")
    finally:
        await bot.close()
        await dp.storage.close()
        await dp.storage.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
