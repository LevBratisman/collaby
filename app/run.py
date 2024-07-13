from aiogram import Bot, Dispatcher
import logging
import asyncio

from app.bot.data.uni_data import set_uni_data

from app.core.config import settings

# routers import
from app.bot.handlers.start import start_router
from app.bot.handlers.base import base_router
from app.bot.handlers.profile.base import base_profile_router
from app.bot.handlers.profile.create import create_profile_router
from app.bot.handlers.profile.delete import delete_profile_router
from app.bot.handlers.project.base import base_project_router
from app.bot.handlers.project.create import create_project_router
from app.bot.handlers.search.project import search_project_router
from app.bot.handlers.search.profile import search_profile_router


# Initialize Bot and Dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


# Connect handlers
dp.include_router(start_router)
dp.include_router(base_profile_router)
dp.include_router(create_profile_router)
dp.include_router(delete_profile_router)
dp.include_router(base_project_router)
dp.include_router(create_project_router)
dp.include_router(search_project_router)
dp.include_router(search_profile_router)
dp.include_router(base_router)


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


