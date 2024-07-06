from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.common.repository.user_repository import UserRepository
from app.common.repository.uni_repository import UniRepository
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.inline.base import get_callback_btns
from app.bot.keyboards.inline.uni import get_uni_btns

start_router = Router()

class Start(StatesGroup):
    telegram_id = State()
    username = State()
    uni_id = State()


@start_router.message(CommandStart())
async def start(
    message: Message,
    state: FSMContext
):
    await state.clear()
    
    if not message.from_user.username:
        await message.answer("Невозможно определить имя пользователя")
        return
    
    user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
    
    if user:
        if user.username != message.from_user.username:
            await UserRepository.update(model_id=user.id, username=message.from_user.username)
        await message.answer("Добро пожаловать в Collaby!", reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))
        return
           
    await state.set_state(Start.uni_id)
    await state.update_data(username=message.from_user.username)
    await state.update_data(telegram_id=message.from_user.id)
    
    await message.answer("С какого вы университета?", reply_markup=await get_uni_btns())
    
    
@start_router.callback_query(StateFilter(Start.uni_id), F.data)
async def set_uni(
    callback: CallbackQuery, 
    state: FSMContext
):
    uni = await UniRepository.get_one_or_none(short_name=callback.data)
    await state.update_data(uni_id=uni.id)
        
    user_data = await state.get_data()
    
    await UserRepository.add(**user_data)
    await callback.message.edit_text("Отлично!")
    
    await callback.message.answer("Добро пожаловать в Collaby!", reply_markup=await get_menu_keyboard(telegram_id=callback.from_user.id))