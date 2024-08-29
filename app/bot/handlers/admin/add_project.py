from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, StateFilter, Command
from random import randrange

from app.bot.filters.admin import IsAdmin
from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.invite_repository import InviteRepository
from app.bot.keyboards.inline.pagination import InviteCallBack
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.reply.admin import get_admin_keyboard
from app.bot.utils.card_generator import get_admin_statistics_card
from app.bot.handlers.project.create import refill_project
from app.bot.keyboards.inline.uni import get_uni_btns
from app.common.repository.uni_repository import UniRepository
from app.bot.handlers.admin.base import admin_panel
from app.bot.keyboards.inline.topic import get_topic_btns


admin_add_project_router = Router()
admin_add_project_router.message.filter(IsAdmin())

class AddProject(StatesGroup):
    name = State()
    topic = State()
    info = State()
    requirements = State()
    image = State()
    uni_id = State()
    user_id = State()
    project_id = State()



@admin_add_project_router.message(StateFilter(None), F.text == "Добавить проект")
async def add_project(message: Message, state: FSMContext):  
    await state.set_state(AddProject.name)  
    await message.answer("Введите название проекта", reply_markup=await get_keyboard("Отмена"))
    
    
@admin_add_project_router.message(StateFilter(AddProject), F.text == "Отмена")
async def reject(message: Message, state: FSMContext):
    await state.clear()
    await admin_panel(message, state)
    
    
@admin_add_project_router.message(StateFilter(AddProject.name), F.text)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProject.topic)
    
    await message.answer("Из какой сферы ваш проект?", reply_markup=await get_topic_btns())
    
    
@admin_add_project_router.callback_query(StateFilter(AddProject.topic), F.data)
async def set_topic(callback: CallbackQuery, state: FSMContext):
    await state.update_data(topic=callback.data)
    await state.set_state(AddProject.info)
    await callback.answer(callback.data)
    
    await callback.message.edit_text("Расскажите немного о своем проекте")
    
    
@admin_add_project_router.message(StateFilter(AddProject.info), F.text)
async def set_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await state.set_state(AddProject.requirements)
    
    await message.answer("Почти финиш! Расскажите о требованиях к участникам")
    
    
@admin_add_project_router.message(StateFilter(AddProject.requirements), F.text)
async def set_skills(message: Message, state: FSMContext):
    await state.update_data(requirements=message.text)
    await state.set_state(AddProject.image)
    
    await message.answer("Отправьте фотографию")
    

@admin_add_project_router.message(StateFilter(AddProject.image), F.photo)
async def set_image(message: Message, state: FSMContext):
    user = await UserRepository.get_one_bot()
    
    await state.update_data(image=message.photo[-1].file_id)
    await state.update_data(user_id=user.id)
    await state.update_data(uni_id=user.uni_id)
    
    project_data = await state.get_data()
    
    await ProjectRepository.add(**project_data)
    
    await message.answer("Вы успешно опубликовали проект")
    await state.clear()
    
    await admin_panel(message, state)