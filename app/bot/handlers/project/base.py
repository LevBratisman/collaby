from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter

from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.bot.keyboards.inline.pagination import ProjectCallBack
from app.common.repository.request_repository import RequestRepository
from app.common.repository.report_repository import ReportRepository
from app.common.repository.invite_repository import InviteRepository
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.utils.keyboard_processing import get_project_kb
from app.bot.handlers.project.create import refill_project

base_project_router = Router()

@base_project_router.message(StateFilter(None), F.text == "👥Мои проекты")
async def my_projects(message: Message):
    
    user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)

    if user.is_banned:
        await message.answer('Ваш профиль заблокирован')
        return
    
    projects = await ProjectRepository.get_all(user_id=user.id)
    
    if not projects:
        await message.answer("У вас нет проектов", reply_markup=await get_keyboard("Опубликовать проект", "Назад"))
        return
    
    
    media, keyboard = await get_project_kb(projects=projects, page=1)
    
    await message.answer('Ваши проекты', reply_markup=await get_keyboard("Опубликовать проект", "Назад"))
    
    await message.answer_photo(media.media, caption=media.caption, reply_markup=keyboard)
    
    
@base_project_router.callback_query(ProjectCallBack.filter())
async def delete_project(callback: CallbackQuery, callback_data: ProjectCallBack, state: FSMContext):  
    print(callback.data)
    if callback_data.action == "delete":
        await ReportRepository.delete_by(project_id=callback_data.project_id)
        await RequestRepository.delete_by(project_id=callback_data.project_id)
        await InviteRepository.delete_by(project_id=callback_data.project_id)
        await ProjectRepository.delete(model_id=callback_data.project_id)
        await callback.answer("Проект удален")
        
        user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
        projects = await ProjectRepository.get_all(user_id=user.id)
        
        if not projects:
            await callback.message.delete()
            await callback.message.answer("У вас нет проектов. хотите опубликовать?", reply_markup=await get_keyboard("Опубликовать проект", "В другой раз"))
            return
        
        media, keyboard = await get_project_kb(projects=projects, page=1 if callback_data.page == 1 else callback_data.page - 1)
        
        await callback.message.edit_media(media=media, 
                                      reply_markup=keyboard)
        
    elif callback_data.action == "refill":
        await refill_project(callback=callback, state=state)
        
    else:
        user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
        projects = await ProjectRepository.get_all(user_id=user.id)
            
        media, reply_markup = await get_project_kb(
            projects=projects,
            page=callback_data.page
        )
            
        await callback.message.edit_media(media=media, 
                                        reply_markup=reply_markup)
        await callback.answer()
    
    
@base_project_router.message(F.text == "Назад")
async def reject(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))