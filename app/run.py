from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import logging
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiogram.types import Update
import uvicorn

from app.bot.data.uni_data import set_uni_data
from app.bot.commands.cmd_list import private

from app.core.config import settings

# routers import
from app.bot.handlers.start import start_router
from app.bot.handlers.base import base_router
from app.bot.commands.base import cmd_base_router
from app.bot.handlers.premium.base import base_premium_router
from app.bot.handlers.profile.base import base_profile_router
from app.bot.handlers.profile.create import create_profile_router
from app.bot.handlers.profile.delete import delete_profile_router
from app.bot.handlers.project.base import base_project_router
from app.bot.handlers.project.create import create_project_router
from app.bot.handlers.search.project import search_project_router
from app.bot.handlers.search.profile import search_profile_router
from app.bot.handlers.invites import base_invite_router
from app.bot.handlers.admin.base import base_admin_router
from app.bot.handlers.admin.add_bot import admin_add_bot_router
from app.bot.handlers.admin.add_project import admin_add_project_router
from app.bot.handlers.admin.moderation import admin_moderation_router
from app.bot.handlers.search_settings.base import base_search_settings_router
from app.bot.handlers.requests import base_request_router
from app.bot.handlers.search_settings.profile import base_search_settings_profile_router
from app.bot.handlers.search_settings.project import base_search_settings_project_router


@asynccontextmanager
async def lifespan(app):
    logging.info("Starting bot")
    await set_uni_data()
    dp.shutdown.register(on_shutdown)
    await bot.set_my_commands(private)
    await bot.delete_webhook(drop_pending_updates=True)
    yield
    

app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "POST"])
async def webhook(update: dict):
    telegram_update = Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)
    return 'get'


# Initialize Bot and Dispatcher
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


# Connect handlers
dp.include_router(start_router)
dp.include_router(base_profile_router)
dp.include_router(cmd_base_router)
dp.include_router(create_profile_router)
dp.include_router(delete_profile_router)
dp.include_router(base_project_router)
dp.include_router(create_project_router)
dp.include_router(search_project_router)
dp.include_router(search_profile_router)
dp.include_router(base_invite_router)
dp.include_router(base_request_router)
dp.include_router(base_search_settings_router)
dp.include_router(base_search_settings_profile_router)
dp.include_router(base_search_settings_project_router)
dp.include_router(base_premium_router)
dp.include_router(base_admin_router)
dp.include_router(admin_add_bot_router)
dp.include_router(admin_add_project_router)
dp.include_router(admin_moderation_router)

dp.include_router(base_router)


async def on_shutdown(bot):
    logging.info("Shutting down bot")


async def main():
    await set_uni_data()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(private)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # try:
    #     # uvicorn.run(app, host="127.0.0.1", port=80)
    # except KeyboardInterrupt:
    #     print("error")


