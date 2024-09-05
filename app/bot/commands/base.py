import asyncio
from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.handlers.search.profile import start_search_profile
from app.bot.handlers.search.project import start_search_project

from app.bot.text.common import help_text

cmd_base_router = Router()


class SendFeedback(StatesGroup):
    feedback = State()


@cmd_base_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Меню", reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))
            
    
@cmd_base_router.message(Command("people"))
async def cmd_search_profile(message: Message, state: FSMContext):
    await state.clear()
    await start_search_profile(message, state)
    
    
@cmd_base_router.message(Command("projects"))
async def cmd_search_project(message: Message, state: FSMContext):
    await state.clear()
    await start_search_project(message, state)
    
    
@cmd_base_router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(help_text, reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))
    
    
@cmd_base_router.message(Command("feedback"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('По всем вопросам обращайтесь к @bratisman', reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))