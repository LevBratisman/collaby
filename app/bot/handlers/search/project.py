from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from app.common.repository.filter_repository import FilterRepository
from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.bot.utils.search import transform_filter_for_search_projects
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.inline.base import get_callback_btns
from app.bot.keyboards.inline.card import get_profile_search_btns
from app.bot.utils.card_generator import get_project_card


search_project_router = Router()

@search_project_router.message(StateFilter(None), F.text.in_(["Далее", "💡Искать проекты"]))
async def start_search_project(message: Message):
            
        user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
        user_filter = await FilterRepository.get_filter_by_telegram_id(telegram_id=message.from_user.id)
        
        if user_filter:
            user_filter = await transform_filter_for_search_projects(user_filter)            
        
        target_projects = await ProjectRepository.get_projects_by_filter(user_id=message.from_user.id, **user_filter)
        
        if target_projects:
            iter = user.project_iter
            await message.answer("🔍", reply_markup=await get_keyboard("Назад", "Далее"))
            try:
                await UserRepository.set_project_iterator(message.from_user.id, iter + 1)
                user_description = await get_project_card(target_projects[iter].id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_profile_search_btns(target_projects[iter].id))
            except IndexError:
                await UserRepository.set_project_iterator(message.from_user.id, 0)
                iter = 0
                user_description = await get_project_card(target_projects[iter].id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_profile_search_btns(target_projects[iter].id))
        else:
            await message.answer("По вашему запросу ничего не найдено")