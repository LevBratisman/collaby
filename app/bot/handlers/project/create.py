from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.bot.utils.keyboard_processing import get_project_kb
from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.bot.keyboards.inline.pagination import ProjectCallBack
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.inline.topic import get_topic_btns

create_project_router = Router()


class CreateProject(StatesGroup):
    name = State()
    topic = State()
    info = State()
    requirements = State()
    image = State()
    uni_id = State()
    user_id = State()
    is_updated = State()
    project_id = State()


@create_project_router.message(StateFilter(None), F.text == "Опубликовать проект")
async def post_project(message: Message, state: FSMContext):
    await state.update_data(is_updated=False)
    await state.set_state(CreateProject.name)
    
    await message.answer("Введите название проекта", reply_markup=await get_keyboard("Отмена"))
    
@create_project_router.callback_query(StateFilter(None), F.data.contains("project_refill"))
async def refill_project(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    await state.update_data(is_updated=True)
    await state.update_data(project_id=int(callback.data.split(':')[-2]))
        
    await state.set_state(CreateProject.name)
    await callback.answer('Изменение данных проекта')
        
    await callback.message.answer("Введите название проекта", reply_markup=await get_keyboard("Отмена"))
    
    
@create_project_router.message(StateFilter(CreateProject), F.text == "Отмена")
async def reject(message: Message, state: FSMContext):
    await state.clear()
    await my_projects(message)
    
    
@create_project_router.message(StateFilter(CreateProject.name), F.text)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateProject.topic)
    
    await message.answer("Из какой сферы ваш проект?", reply_markup=await get_topic_btns())
    
    
@create_project_router.callback_query(StateFilter(CreateProject.topic), F.data)
async def set_topic(callback: CallbackQuery, state: FSMContext):
    await state.update_data(topic=callback.data)
    await state.set_state(CreateProject.info)
    await callback.answer(callback.data)
    
    await callback.message.edit_text("Расскажите немного о своем проекте")
    
    
@create_project_router.message(StateFilter(CreateProject.info), F.text)
async def set_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await state.set_state(CreateProject.requirements)
    
    await message.answer("Почти финиш! Расскажите о требованиях к участникам")
    
    
@create_project_router.message(StateFilter(CreateProject.requirements), F.text)
async def set_skills(message: Message, state: FSMContext):
    await state.update_data(requirements=message.text)
    await state.set_state(CreateProject.image)
    
    await message.answer("Отправьте фотографию")
    

@create_project_router.message(StateFilter(CreateProject.image), F.photo)
async def set_image(message: Message, state: FSMContext):
    user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
    
    await state.update_data(image=message.photo[-1].file_id)
    await state.update_data(user_id=user.id)
    await state.update_data(uni_id=user.uni_id)
    
    project_data = await state.get_data()
    
    is_updated = project_data.pop('is_updated')
    try:
        project_id = project_data.pop('project_id')
    except KeyError:
        pass
    
    if is_updated:
        await ProjectRepository.update(model_id=project_id, **project_data)
    else:
        await ProjectRepository.add(**project_data)
    
    await message.answer("Вы успешно опубликовали проект", reply_markup=await get_keyboard("Опубликовать проект", "Назад"))
    await state.clear()
    
    await my_projects(message)
    

@create_project_router.message(StateFilter(None), F.text == "Мои проекты")
async def my_projects(message: Message):
    user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
    projects = await ProjectRepository.get_all(user_id=user.id)
    
    if not projects:
        await message.answer("У вас нет проектов", reply_markup=await get_keyboard("Опубликовать проект", "Назад"))
        return
    
    media, keyboard = await get_project_kb(projects=projects, page=1)
    await message.answer('Ваши проекты', reply_markup=await get_keyboard("Опубликовать проект", "Назад"))
    
    await message.answer_photo(media.media, caption=media.caption, reply_markup=keyboard)
    
    
    
    