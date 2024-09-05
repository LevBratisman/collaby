from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.common.repository.user_repository import UserRepository
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.inline.card import get_profile_btns, get_profile_delete_btns
from app.bot.text.common import unfilled_profile_text, delete_profile_confirm_text
from app.bot.utils.card_generator import get_profile_card

delete_profile_router = Router()

class DeleteProfile(StatesGroup):
    confirmation = State()

reset_data = {
    'is_authorized': False,
    'name': None,
    'info': None,
    'skills': None,
    'image': None,
    'topic': None
}

@delete_profile_router.callback_query(StateFilter(None), F.data.startswith("delete_profile"))
async def delete_profile(callback: CallbackQuery, state: FSMContext):
    
    user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
    user_info = await get_profile_card(telegram_id=callback.from_user.id)
    
    await state.set_state(DeleteProfile.confirmation)
    
    confirmation_info = InputMediaPhoto(media=user_info["photo"], caption=delete_profile_confirm_text)
    
    await callback.message.edit_media(confirmation_info, reply_markup=await get_profile_delete_btns(user_id=user.id))
    await callback.answer('Удаление анкеты')
    
    
@delete_profile_router.callback_query(StateFilter(DeleteProfile.confirmation), F.data.startswith("delete_profile_"))
async def delete_profile_confirm(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split('_')[-1])
    
    await UserRepository.update(model_id=user_id, **reset_data)
    
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Ваша анкета удалена!")
    await state.clear()
    
    
@delete_profile_router.callback_query(StateFilter(DeleteProfile.confirmation), F.data.startswith("cancel_delete_profile"))
async def cancel_delete_profile(callback: CallbackQuery, state: FSMContext):
    
    user_info = await get_profile_card(telegram_id=callback.from_user.id)
    user_id = int(callback.data.split('_')[-1])
    
    profile_info = InputMediaPhoto(media=user_info['photo'], caption=user_info['description'])
    
    await callback.answer()
    await callback.message.edit_media(media=profile_info, reply_markup=await get_profile_btns(user_id))
    await state.clear()