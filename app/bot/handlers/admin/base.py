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

base_admin_router = Router()

@base_admin_router.message(StateFilter('*'), Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Админ панель", reply_markup=await get_admin_keyboard())
    
    
@base_admin_router.message(StateFilter(None), F.text == "Статистика")
async def statistics(message: Message, state: FSMContext):
    await state.clear()
    
    await message.answer(text=await get_admin_statistics_card(), reply_markup=await get_admin_keyboard())