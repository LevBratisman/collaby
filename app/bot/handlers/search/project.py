from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from app.common.repository.filter_repository import FilterRepository
from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.request_repository import RequestRepository
from app.common.repository.report_repository import ReportRepository
from app.bot.keyboards.inline.report import ReportCallBack
from app.bot.utils.search import transform_filter_for_search_projects
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.inline.base import get_callback_btns
from app.bot.keyboards.inline.report import get_report_reasons_for_project
from app.bot.keyboards.inline.card import get_project_search_btns
from app.bot.utils.card_generator import get_project_card

class RequestProject(StatesGroup):
    message = State()
    
class ReportProject(StatesGroup):
    reason = State()

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
                                           reply_markup=await get_project_search_btns(target_projects[iter].id))
            except IndexError:
                await UserRepository.set_project_iterator(message.from_user.id, 1)
                iter = 0
                user_description = await get_project_card(target_projects[iter].id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_project_search_btns(target_projects[iter].id))
        else:
            await message.answer("По вашему запросу ничего не найдено")
            

@search_project_router.callback_query(StateFilter(None), F.data.startswith('request_project_'))
async def invite_user(callback: CallbackQuery, bot: Bot):
    target_project_id = int(callback.data.split('_')[-1])
    target_project = await ProjectRepository.get_by_id(model_id=target_project_id)
    sender_user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
    
    if not sender_user.is_banned:
        if sender_user.is_authorized:
            if target_project.is_banned:
                await callback.answer("Этот проект заблокирован")
            else:
                request = await RequestRepository.get_one_or_none(project_id=target_project.id, user_id=sender_user.id)
                
                if request:
                    await callback.answer("Вы уже подали заявку на этот проект")
                else:
                    request_data = {
                        "project_id": target_project.id,
                        "user_id": sender_user.id,
                    }

                    await RequestRepository.add(**request_data)
                    creator = await UserRepository.get_by_id(model_id=target_project.user_id)
                    await bot.send_message(creator.telegram_id, f"Кто-то хочет вступить в проект {target_project.name}!")
                    await callback.answer("Заявка отправлена")
                    
        else:
            await callback.answer("Пожалуйста, заполните анкету")
    else:
        await callback.answer("Ваш профиль заблокирован")
        
        
# --------------------------------------- REPORT PROJECT ---------------------------------------


@search_project_router.callback_query(StateFilter(None), F.data.startswith('report_project_'))
async def invite_user(callback: CallbackQuery, state: FSMContext):
    target_project_id = int(callback.data.split('_')[-1])
    target_project = await ProjectRepository.get_by_id(model_id=target_project_id)
    reporter = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
    
    if not reporter.is_banned:
        if reporter.is_authorized:
            if not target_project.is_banned:
                report = await ReportRepository.get_one_or_none(project_id=target_project_id, sender_id=reporter.id)
                if not report:
                    await state.set_state(ReportProject.reason)
                    project_info = InputMediaPhoto(media=target_project.image, caption='Пожалуйста, выберите причину жалобы')
                    await callback.answer("Выберите причину жалобы")
                    await callback.message.edit_media(project_info, reply_markup=await get_report_reasons_for_project(sender_id=reporter.id, target_id=target_project_id))
                else:
                    await callback.answer("Вы уже отправили жалобу на этот проект")
            else:
                await callback.answer("Этот проект уже заблокирован")
        else:
            await callback.answer("Вы не заполнили профиль")
    else:
        await callback.answer("Вы были забанены")
        
        
@search_project_router.callback_query(StateFilter(ReportProject.reason), ReportCallBack.filter())
async def report_user(callback: CallbackQuery, callback_data: ReportCallBack, state: FSMContext):
    
    if callback_data.action == "report":
        report_data = {
            "project_id": callback_data.target_id,
            "to_project": True,
            "sender_id": callback_data.sender_id,
            "reason": callback_data.reason
        }
            
        await ReportRepository.add(**report_data)
        await callback.answer("Жалоба отправлена")
        
    project_description = await get_project_card(callback_data.target_id)
            
    project_description_media = InputMediaPhoto(media=project_description['photo'], caption=project_description['description'])
    await callback.message.edit_media(project_description_media, reply_markup=await get_project_search_btns(callback_data.target_id))
    if callback_data.action == "cancel":
        await callback.answer()
    await state.clear()