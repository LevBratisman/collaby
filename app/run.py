from aiogram import Bot, Dispatcher
import logging
import asyncio

from app.core.config import settings


# Initialize Bot and Dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")


