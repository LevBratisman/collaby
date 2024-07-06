from aiogram import Bot, Dispatcher
import logging
import asyncio

from app.bot.data.uni_data import set_uni_data

from app.core.config import settings

# routers import
from app.bot.handlers.start import start_router


# Initialize Bot and Dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


# Connect handlers
dp.include_router(start_router)


async def main():
    await set_uni_data()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")


