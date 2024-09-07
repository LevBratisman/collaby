from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.common.repository.user_repository import UserRepository
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.inline.topic import get_topic_btns
from app.bot.handlers.profile.base import my_profile

create_profile_router = Router()


class CreateProfile(StatesGroup):
    name = State()
    topic = State()
    info = State()
    skills = State()
    image = State()
    is_authorized = State()


@create_profile_router.message(StateFilter(CreateProfile), F.text == "Отмена")
async def reject(message: Message, state: FSMContext):
    await state.clear()
    await my_profile(message)


@create_profile_router.message(StateFilter(None), F.text == "Заполнить анкету🚀")
async def fill_profile(message: Message, state: FSMContext):
    await state.set_state(CreateProfile.name)
    
    await message.answer("Как вас зовут?", reply_markup=await get_keyboard("Отмена"))
    
@create_profile_router.callback_query(StateFilter(None), F.data.contains("refill_profile"))
async def refill_profile(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CreateProfile.name)
    await callback.answer('Заполнение анкеты')
    
    await callback.message.answer("Как вас зовут?", reply_markup=await get_keyboard("Отмена"))


    
@create_profile_router.message(StateFilter(CreateProfile.name), F.text)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateProfile.topic)
    
    await message.answer("В какой сфере вы развиваетесь?", reply_markup=await get_topic_btns())

@create_profile_router.message(StateFilter(CreateProfile.name))
async def set_name(message: Message, state: FSMContext):    
    await message.answer("Введите ваше имя (текст)")


    
@create_profile_router.callback_query(StateFilter(CreateProfile.topic), F.data)
async def set_topic(callback: CallbackQuery, state: FSMContext):
    await state.update_data(topic=callback.data)
    await state.set_state(CreateProfile.info)
    await callback.answer(callback.data)
    
    await callback.message.edit_text("Напишите немного о себе")

@create_profile_router.message(StateFilter(CreateProfile.topic))
async def set_topic(message: Message, state: FSMContext):    
    await message.answer("Используйте предложенные варианты", reply_markup=await get_topic_btns())
    
    

@create_profile_router.message(StateFilter(CreateProfile.info), F.text)
async def set_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await state.set_state(CreateProfile.skills)
    
    await message.answer("Почти финиш! Перечислите ваши навыки")

@create_profile_router.message(StateFilter(CreateProfile.info))
async def set_info(message: Message, state: FSMContext):    
    await message.answer("Напишите о себе (Введите текст)")  
    

    
@create_profile_router.message(StateFilter(CreateProfile.skills), F.text)
async def set_skills(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await state.set_state(CreateProfile.image)
    
    await message.answer("Отправьте свою фотографию")

@create_profile_router.message(StateFilter(CreateProfile.skills))
async def set_skills(message: Message, state: FSMContext):    
    await message.answer("Перечислите ваши навыки (Введите текст)")

    

@create_profile_router.message(StateFilter(CreateProfile.image), F.photo)
async def set_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await state.update_data(is_authorized=True)
    
    user_data = await state.get_data()
    
    user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
    await UserRepository.update(model_id=user.id, **user_data)
    
    await message.answer("Вы успешно заполнили анкету", reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))
    
    await my_profile(message, state)


@create_profile_router.message(StateFilter(CreateProfile.image))
async def set_image(message: Message, state: FSMContext):
    await message.answer('Загрузите изображение')
    
    
    
    