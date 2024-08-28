from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

import datetime

from app.common.repository.filter_repository import FilterRepository
from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.report_repository import ReportRepository
from app.common.repository.invite_repository import InviteRepository
from app.common.repository.banned_user_repository import BannedUserRepository
from app.bot.keyboards.inline.project import InviteUserCallBack
from app.bot.keyboards.inline.report import ReportCallBack
from app.bot.utils.search import transform_filter_for_search_people
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.inline.base import get_callback_btns
from app.bot.keyboards.inline.report import get_report_reasons_for_user
from app.bot.keyboards.inline.project import get_projects
from app.bot.keyboards.inline.card import get_profile_search_btns
from app.bot.utils.card_generator import get_profile_card

from app.bot.utils.ban_system.ban_profile import ban_profile, unban_profile


class InviteProfile(StatesGroup):
    project = State()
    message = State()
    
class ReportProfile(StatesGroup):
    reason = State()

search_profile_router = Router()

@search_profile_router.message(StateFilter(None), F.text.in_(["Следующий", "🔍Искать людей"]))
async def start_search_profile(message: Message):
            
        user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
        
        if user.is_banned:
            banned_user = await BannedUserRepository.get_one_or_none(user_id=user.id)
            if banned_user.date_end < datetime.datetime.now(tz=datetime.timezone.utc):
                await unban_profile(user)
        
        user_filter = await FilterRepository.get_filter_by_telegram_id(telegram_id=message.from_user.id)
        
        if user_filter:
            user_filter = await transform_filter_for_search_people(user_filter) 
            
        target_users = await UserRepository.get_users_by_filter(user_id=user.id, **user_filter)
        if target_users:
            iter = user.person_iter
            await message.answer("🔍", reply_markup=await get_keyboard("Назад", "Следующий"))
            try:
                await UserRepository.set_person_iterator(message.from_user.id, iter + 1)
                user_description = await get_profile_card(target_users[iter].telegram_id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_profile_search_btns(target_users[iter].id))
            except IndexError:
                await UserRepository.set_person_iterator(message.from_user.id, 1)
                iter = 0
                user_description = await get_profile_card(target_users[iter].telegram_id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_profile_search_btns(target_users[iter].id))
        else:
            await message.answer("По вашему запросу ничего не найдено")
        

# --------------------------------------- INVITE USER TO PROJECT ---------------------------------------

@search_profile_router.callback_query(StateFilter(None), F.data.startswith('invite_profile_'))
async def invite_user(callback: CallbackQuery, state: FSMContext):
    target_user_id = int(callback.data.split('_')[-1])
    target_user = await UserRepository.get_by_id(model_id=target_user_id)
    inviter = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
    
    if inviter.is_banned:
        await callback.answer("Вы были забанены")
        return
    
    if target_user.is_authorized and not target_user.is_banned:
        existed_projects = await ProjectRepository.get_all(user_id=inviter.id)
        if existed_projects:
            projects_info = InputMediaPhoto(media=target_user.image, caption='Пожалуйста, выберите проект для приглашения')
            await callback.answer("Выбор проекта")
            await callback.message.edit_media(projects_info, reply_markup=await get_projects(projects=existed_projects, target_user_id=target_user_id, sender_user_id=inviter.id))
            await state.set_state(InviteProfile.project)
        else:
            await callback.answer("Вы еще не опубликовали проекты")
    else:
        await callback.answer("Этот пользователь удалил свою анкету")
        
        
@search_profile_router.callback_query(StateFilter(InviteProfile.project), InviteUserCallBack.filter())
async def invite_user_to_project(callback: CallbackQuery, callback_data: InviteUserCallBack, state: FSMContext, bot: Bot):
    
    if callback_data.action == "invite":
        invite = await InviteRepository.get_one_or_none(project_id=callback_data.project_id, user_id=callback_data.target_user_id, sender_id=callback_data.sender_user_id)
        if not invite:
            invite_data = {
                "project_id": callback_data.project_id,
                "user_id": callback_data.target_user_id,
                "sender_id": callback_data.sender_user_id
            }
            
            await InviteRepository.add(**invite_data)
            target_user = await UserRepository.get_by_id(model_id=callback_data.target_user_id)
            if target_user.telegram_id > 10000:
                await bot.send_message(target_user.telegram_id, f"Кто-то пригласил вас в свой проект!")
            await callback.answer("Приглашение отправлено")
            
        else:
            await callback.answer("Вы уже приглашали этого пользователя на этот проект")
            return
        
    user = await UserRepository.get_by_id(model_id=callback_data.target_user_id)
    user_description = await get_profile_card(user.telegram_id)
            
    user_description_media = InputMediaPhoto(media=user_description['photo'], caption=user_description['description'])
    await callback.message.edit_media(user_description_media, reply_markup=await get_profile_search_btns(callback_data.target_user_id))
    if callback_data.action == "cancel":
        await callback.answer()
    await state.clear()
    
    
# --------------------------------------- REPORT USER ---------------------------------------


@search_profile_router.callback_query(StateFilter(None), F.data.startswith('report_profile_'))
async def invite_user(callback: CallbackQuery, state: FSMContext):
    target_user_id = int(callback.data.split('_')[-1])
    target_user = await UserRepository.get_by_id(model_id=target_user_id)
    reporter = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
    
    if not reporter.is_banned:
        if reporter.is_authorized:
            if target_user.is_authorized and not target_user.is_banned:
                report = await ReportRepository.get_one_or_none(user_id=target_user_id, sender_id=reporter.id)
                if not report:
                    await state.set_state(ReportProfile.reason)
                    user_info = InputMediaPhoto(media=target_user.image, caption='Пожалуйста, выберите причину жалобы')
                    await callback.answer("Выберите причину жалобы")
                    await callback.message.edit_media(user_info, reply_markup=await get_report_reasons_for_user(sender_id=reporter.id, target_id=target_user_id))
                else:
                    await callback.answer("Вы уже отправили жалобу на этого пользователя")
            else:
                await callback.answer("Этот пользователь не доступен")
        else:
            await callback.answer("Вы не заполнили профиль")
    else:
        await callback.answer("Вы были забанены")
        
        
@search_profile_router.callback_query(StateFilter(ReportProfile.reason), ReportCallBack.filter())
async def report_user(callback: CallbackQuery, callback_data: ReportCallBack, state: FSMContext, bot: Bot):
    
    if callback_data.action == "report":
        report_data = {
            "user_id": callback_data.target_id,
            "to_project": False,
            "sender_id": callback_data.sender_id,
            "reason": callback_data.reason
        }
            
        await ReportRepository.add(**report_data)
        await callback.answer("Жалоба отправлена")
        
    user = await UserRepository.get_by_id(model_id=callback_data.target_id)
    await UserRepository.update(model_id=user.id, claim_count=user.claim_count + 1)
    
    if user.claim_count == 4:
        await ban_profile(user)
        if user.telegram_id > 10000:
            await bot.send_message(user.telegram_id, "Ваш профиль был забанен. Причина: " + callback_data.reason)
        
    user_description = await get_profile_card(user.telegram_id)
            
    user_description_media = InputMediaPhoto(media=user_description['photo'], caption=user_description['description'])
    await callback.message.edit_media(user_description_media, reply_markup=await get_profile_search_btns(callback_data.target_id))
    if callback_data.action == "cancel":
        await callback.answer()
    await state.clear()
