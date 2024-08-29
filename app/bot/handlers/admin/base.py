from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, StateFilter, Command

from app.bot.filters.admin import IsAdmin
from app.bot.utils.ban_system.ban_profile import unban_profile
from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.invite_repository import InviteRepository
from app.bot.keyboards.inline.pagination import InviteCallBack
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.reply.admin import get_admin_keyboard
from app.bot.utils.card_generator import get_admin_statistics_card, get_profile_card
from app.bot.handlers.project.create import refill_project

base_admin_router = Router()
base_admin_router.message.filter(IsAdmin())


class UnbanUser(StatesGroup):
    telegram_id = State()


class GetUserCard(StatesGroup):
    telegram_id = State()


@base_admin_router.message(StateFilter('*'), Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Админ панель", reply_markup=await get_admin_keyboard())
    
    
@base_admin_router.message(StateFilter(None), F.text == "Статистика")
async def statistics(message: Message, state: FSMContext):
    await state.clear()
    
    await message.answer(text=await get_admin_statistics_card(), reply_markup=await get_admin_keyboard())


@base_admin_router.message(StateFilter(None), F.text == "Разблокировать пользователя")
async def get_user_id(message: Message, state: FSMContext):
    await state.set_state(UnbanUser.telegram_id)

    await message.answer('Введите user_id')


@base_admin_router.message(StateFilter(UnbanUser.telegram_id), F.text)
async def unban(message: Message, state: FSMContext):
    user = await UserRepository.get_by_telegram_id(telegram_id=int(message.text))

    try:
        await unban_profile(user)
    except:
        await message.answer('Такой пользователь не зарегистрирован')
        await state.clear()
        return
    
    await message.answer('Пользователь разблокирован')
    await state.clear()


@base_admin_router.message(StateFilter(None), F.text=='Просмотреть анкету пользователя')
async def get_user_id(message: Message, state: FSMContext):
    await state.set_state(GetUserCard.telegram_id)

    await message.answer('Введите user_id')



@base_admin_router.message(StateFilter(GetUserCard.telegram_id), F.text)
async def get_user_card(message: Message, state: FSMContext):
    user = await UserRepository.get_by_telegram_id(telegram_id=int(message.text))

    try:
        user_description = await get_profile_card(user.telegram_id)
        await message.answer_photo(user_description['photo'], caption=user_description['description'])
    except:
        await message.answer('Такой пользователь не зарегистрирован')
        await state.clear()
        return
    
    await state.clear()