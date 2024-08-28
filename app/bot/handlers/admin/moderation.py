from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command

from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.invite_repository import InviteRepository
from app.bot.keyboards.inline.pagination import InviteCallBack
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.reply.admin import get_admin_keyboard
from app.bot.utils.card_generator import get_admin_statistics_card
from app.bot.handlers.project.create import refill_project

admin_moderation_router = Router()

@admin_moderation_router.message(F.text=='Модерация пользователей')
async def moderation_users(message: Message, state: FSMContext):
    await message.answer("Модерация пользователей")


@admin_moderation_router.message(F.text=='Модерация проектов')
async def moderation_projects(message: Message, state: FSMContext):
    await message.answer("Модерация проектов")