from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter

from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.invite_repository import InviteRepository
from app.bot.keyboards.inline.pagination import InviteCallBack
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.utils.keyboard_processing import get_invite_kb
from app.bot.handlers.project.create import refill_project
from app.bot.utils.card_generator import get_search_settings_card
from app.bot.keyboards.inline.card import get_search_settings_btns

base_search_settings_router = Router()

@base_search_settings_router.message(StateFilter('*'), F.text.contains("⚙️Параметры поиска"))
async def search_setting(message: Message, state: FSMContext):
    await state.clear()
    
    user_search_settings = await get_search_settings_card(telegram_id=message.from_user.id)
    
    await message.answer(user_search_settings['description'], reply_markup=await get_search_settings_btns(telegram_id=message.from_user.id))
    
    
