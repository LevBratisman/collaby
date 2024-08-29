from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.common.repository.user_repository import UserRepository
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.inline.card import get_profile_btns
from app.bot.text.common import unfilled_profile_text
from app.bot.utils.card_generator import get_profile_card

base_profile_router = Router()

@base_profile_router.message(StateFilter('*'), F.text == "🎴Мой профиль")
async def my_profile(message: Message, state: FSMContext):
    await state.clear()

    user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
    
    if user.is_banned:
        await message.answer('Ваш профиль заблокирован')
        return

    if not user.is_authorized:
        await message.answer(unfilled_profile_text, reply_markup=await get_keyboard('Заполнить анкету🚀', 'В другой раз'))
        return
    
    user_info = await get_profile_card(telegram_id=message.from_user.id)
    
    await message.answer("Ваш профиль", reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))
    
    await message.answer_photo(user_info['photo'], caption=user_info['description'], reply_markup=await get_profile_btns(user_id=user.id))
    
    
    
@base_profile_router.message(F.text == "В другой раз")
async def reject(message: Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))