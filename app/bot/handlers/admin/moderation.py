from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command

from app.bot.filters.admin import IsAdmin
from app.bot.keyboards.inline.card import get_project_search_btns
from app.bot.utils.ban_system.ban_profile import ban_profile
from app.bot.utils.ban_system.ban_project import ban_project
from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.invite_repository import InviteRepository
from app.bot.keyboards.inline.pagination import InviteCallBack
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.inline.moderation import (
    get_moderate_kb_for_users, 
    get_moderate_kb_for_projects, 
    ModerationCallBackUser, 
    ModerationCallBackProject
)
from app.bot.utils.card_generator import get_profile_card, get_project_card
from app.bot.handlers.admin.base import admin_panel
from app.common.repository.report_repository import ReportRepository
from app.common.repository.project_repository import ProjectRepository

admin_moderation_router = Router()
admin_moderation_router.message.filter(IsAdmin())


@admin_moderation_router.message(StateFilter(None), F.text=='обратно')
async def back_to_admin(message: Message, state: FSMContext):
    await admin_panel(message, state)
        

@admin_moderation_router.message(StateFilter(None), F.text.in_(["Модерация пользователей", "след"]))
async def start_search_claims_users(message: Message):
            
        user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
            
        target_users = await UserRepository.get_claims_users()

        if target_users:
            iter = user.person_iter
            await message.answer("🔍", reply_markup=await get_keyboard("обратно", "след"))
            try:
                await UserRepository.set_person_iterator(message.from_user.id, iter + 1)
                user_description = await get_profile_card(target_users[iter].telegram_id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_moderate_kb_for_users(target_users[iter].id))
            except IndexError:
                await UserRepository.set_person_iterator(message.from_user.id, 1)
                iter = 0
                user_description = await get_profile_card(target_users[iter].telegram_id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_moderate_kb_for_users(target_users[iter].id))
        else:
            await message.answer("По вашему запросу ничего не найдено")


@admin_moderation_router.callback_query(StateFilter(None), ModerationCallBackUser.filter())
async def report_user(callback: CallbackQuery, callback_data: ModerationCallBackUser, state: FSMContext, bot: Bot):
    
    user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)

    report_data = {
        "user_id": callback_data.target_id,
        "to_project": False,
        "sender_id": user.id,
        "reason": 'ADMIN'
    }
            
    await ReportRepository.add(**report_data)
    await callback.answer("Профиль заблокирован")
        
    banned_user = await UserRepository.get_by_id(model_id=callback_data.target_id)
    await ban_profile(banned_user)
    if not user.is_bot:
        await bot.send_message(banned_user.telegram_id, "Ваш профиль был забанен админом")            



# -------------------------- PROJECT ------------------------------


@admin_moderation_router.message(StateFilter(None), F.text.in_(["Модерация проектов", "->"]))
async def start_search_claims_projects(message: Message):
            
        user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
            
        target_projects = await ProjectRepository.get_claims_projects()

        if target_projects:
            iter = user.project_iter
            await message.answer("🔍", reply_markup=await get_keyboard("обратно", "->"))
            try:
                await UserRepository.set_project_iterator(message.from_user.id, iter + 1)
                user_description = await get_project_card(target_projects[iter].id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_moderate_kb_for_projects(target_projects[iter].id))
            except IndexError:
                await UserRepository.set_project_iterator(message.from_user.id, 1)
                iter = 0
                user_description = await get_project_card(target_projects[iter].id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_moderate_kb_for_projects(target_projects[iter].id))
        else:
            await message.answer("По вашему запросу ничего не найдено")


@admin_moderation_router.callback_query(StateFilter(None), ModerationCallBackProject.filter())
async def report_project(callback: CallbackQuery, callback_data: ModerationCallBackProject, state: FSMContext, bot: Bot):
    
    user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)

    report_data = {
        "project_id": callback_data.target_id,
        "to_project": True,
        "sender_id": user.id,
        "reason": 'ADMIN'
    }
            
    await ReportRepository.add(**report_data)
    await callback.answer("Проект заблокирован")
        
    banned_project = await ProjectRepository.get_by_id(model_id=callback_data.target_id)
    user_creator = await UserRepository.get_by_id(model_id=banned_project.user_id)
    
    await ban_project(banned_project)
    if not user_creator.is_bot:
        await bot.send_message(user.telegram_id, f"Ваш проект {banned_project.name} был забанен админом")