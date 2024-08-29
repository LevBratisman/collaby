from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter

from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.invite_repository import InviteRepository
from app.bot.keyboards.inline.pagination import InviteCallBack
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.utils.keyboard_processing import get_invite_kb
from app.bot.handlers.project.create import refill_project

base_invite_router = Router()

@base_invite_router.message(StateFilter(None), F.text.contains("🔔Приглашения"))
async def my_invites(message: Message):
    
    user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
    
    invites = await InviteRepository.get_all(user_id=user.id)
    
    if not invites:
        await message.answer("У вас нет приглашений", reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))
        return
    
    media, keyboard = await get_invite_kb(invites=invites, page=1)
    
    await message.answer('Ваши приглашения')
    
    await message.answer_photo(media.media, caption=media.caption, reply_markup=keyboard)
    
    
@base_invite_router.callback_query(InviteCallBack.filter())
async def delete_invite(callback: CallbackQuery, callback_data: InviteCallBack, state: FSMContext):  
    if callback_data.action == "delete":
        await InviteRepository.delete(model_id=callback_data.invite_id)
        await callback.answer("Приглашение удалено")
        
        user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
        invites = await InviteRepository.get_all(user_id=user.id)
        
        if not invites:
            await callback.message.answer("У вас нет приглашений", reply_markup=await get_menu_keyboard(telegram_id=callback.from_user.id))
            await callback.message.delete()
            return
        
        media, keyboard = await get_invite_kb(invites=invites, page=1 if callback_data.page == 1 else callback_data.page - 1)
        
        await callback.message.edit_media(media=media, 
                                      reply_markup=keyboard)
        
    else:
        user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
        invites = await InviteRepository.get_all(user_id=user.id)
            
        media, reply_markup = await get_invite_kb(
            invites=invites,
            page=callback_data.page
        )
            
        await callback.message.edit_media(media=media, 
                                        reply_markup=reply_markup)
        await callback.answer()
    