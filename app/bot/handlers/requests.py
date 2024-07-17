from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter

from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.request_repository import RequestRepository
from app.bot.keyboards.inline.pagination import RequestCallBack
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.utils.keyboard_processing import get_request_kb

base_request_router = Router()

@base_request_router.message(StateFilter(None), F.text.contains("🙋🏻‍♂️Заявки"))
async def my_invites(message: Message):
    
    user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
    
    requests = await RequestRepository.get_request_project_info(user_id=user.id)
    
    if not requests:
        await message.answer("У вас нет заявок", reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))
        return
    
    media, keyboard = await get_request_kb(requests=requests, page=1)
    
    await message.answer('Ваши заявки')
    
    await message.answer_photo(media.media, caption=media.caption, reply_markup=keyboard)
    
    
@base_request_router.callback_query(RequestCallBack.filter())
async def delete_invite(callback: CallbackQuery, callback_data: RequestCallBack, state: FSMContext):  
    if callback_data.action == "delete":
        await RequestRepository.delete(model_id=callback_data.request_id)
        await callback.answer("Заявка удалена")
        
        user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
        requests = await RequestRepository.get_request_project_info(user_id=user.id)
        
        if not requests:
            await callback.message.answer("У вас нет заявок", reply_markup=await get_menu_keyboard(telegram_id=callback.from_user.id))
            await callback.message.delete()
            return
        
        media, keyboard = await get_request_kb(requests=requests, page=1 if callback_data.page == 1 else callback_data.page - 1)
        
        await callback.message.edit_media(media=media, 
                                      reply_markup=keyboard)
        
    else:
        user = await UserRepository.get_by_telegram_id(telegram_id=callback.from_user.id)
        requests = await RequestRepository.get_request_project_info(user_id=user.id)
            
        media, reply_markup = await get_request_kb(
            requests=requests,
            page=callback_data.page
        )
            
        await callback.message.edit_media(media=media, 
                                        reply_markup=reply_markup)
        await callback.answer()