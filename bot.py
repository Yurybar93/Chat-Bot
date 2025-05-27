import asyncio
from loader import dp, bot
from utils.logger import logger
from handlers import start, actions, menu, search_menu, setting_menu, genre_search

async def main():
    try:
        logger.info("Starting bot...")
        dp.include_router(genre_search.router)
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
