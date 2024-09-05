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

admin_add_bot_router = Router()
admin_add_bot_router.message.filter(IsAdmin())

class CreateBot(StatesGroup):
    username = State()
    telegram_id = State()
    uni_id = State()
    name = State()
    topic = State()
    info = State()
    skills = State()
    image = State()
    is_authorized = State()



@admin_add_bot_router.message(StateFilter(CreateBot), F.text == "Отмена")
async def reject(message: Message, state: FSMContext):
    await state.clear()
    await admin_panel(message, state)


@admin_add_bot_router.message(F.text=='Добавить бота')
async def add_bot(message: Message, state: FSMContext):
    await state.set_state(CreateBot.uni_id)
    await state.update_data(username=f'bot{randrange(1, 10000000, 1)}')
    await state.update_data(telegram_id=randrange(1, 100000, 1))
    
    await message.answer("С какого вы университета?", reply_markup=await get_uni_btns())


@admin_add_bot_router.callback_query(StateFilter(CreateBot.uni_id), F.data)
async def set_uni(
    callback: CallbackQuery, 
    state: FSMContext
):
    uni = await UniRepository.get_one_or_none(short_name=callback.data)
    await state.update_data(uni_id=uni.id)
    await state.set_state(CreateBot.name)

    await callback.message.answer("Как вас зовут?", reply_markup=await get_keyboard("Отмена"))

    
    
@admin_add_bot_router.message(StateFilter(CreateBot.name), F.text)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateBot.topic)
    
    await message.answer("В какой сфере вы развиваетесь?", reply_markup=await get_topic_btns())
    
    
@admin_add_bot_router.callback_query(StateFilter(CreateBot.topic), F.data)
async def set_topic(callback: CallbackQuery, state: FSMContext):
    await state.update_data(topic=callback.data)
    await state.set_state(CreateBot.info)
    await callback.answer(callback.data)
    
    await callback.message.edit_text("Напишите немного о себе")
    
    
@admin_add_bot_router.message(StateFilter(CreateBot.info), F.text)
async def set_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await state.set_state(CreateBot.skills)
    
    await message.answer("Почти финиш! Перечислите ваши навыки")
    
    
@admin_add_bot_router.message(StateFilter(CreateBot.skills), F.text)
async def set_skills(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await state.set_state(CreateBot.image)
    
    await message.answer("Отправьте свою фотографию")
    

@admin_add_bot_router.message(StateFilter(CreateBot.image), F.photo)
async def set_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await state.update_data(is_authorized=True)
        
    bot_data = await state.get_data()
    bot_data['is_bot'] = True
    await UserRepository.add(**bot_data)
    
    await message.answer("Вы успешно создали бота")
    
    await state.clear()
    await admin_panel(message, state)