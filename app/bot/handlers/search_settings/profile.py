from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, StateFilter

from app.common.repository.user_repository import UserRepository
from app.common.repository.uni_repository import UniRepository
from app.common.repository.filter_repository import FilterRepository
from app.common.repository.project_repository import ProjectRepository
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.reply.menu import get_menu_keyboard
from app.bot.keyboards.inline.topic import get_topic_btns_for_search_settings
from app.bot.keyboards.inline.uni import get_uni_btns
from app.bot.utils.card_generator import get_search_settings_card
from app.bot.keyboards.inline.card import get_search_settings_btns

base_search_settings_profile_router = Router()

class EditSearchSettingsProfileUni(StatesGroup):
    user_id = State()
    uni = State()
    
class EditSearchSettingsProfileTopic(StatesGroup):
    user_id = State()
    topic = State()


# ---------------------------------------------- UNI ----------------------------------------------

@base_search_settings_profile_router.callback_query(StateFilter(None), F.data.contains("edit_filter_profile_uni"))
async def edit_search_setting_profile(callback: CallbackQuery, state: FSMContext):
    
    await state.update_data(user_id=int(callback.data.split('_')[-1]))
    
    await state.set_state(EditSearchSettingsProfileUni.uni)
    await callback.answer()
    await callback.message.edit_text("Выберите университет", reply_markup=await get_uni_btns())
    
    

@base_search_settings_profile_router.callback_query(StateFilter(EditSearchSettingsProfileUni.uni), F.data)
async def edit_search_setting_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    
    filter = await FilterRepository.get_one_or_none(user_id=data['user_id'])
    uni = await UniRepository.get_one_or_none(short_name=callback.data)
    await FilterRepository.update(model_id=filter.id, profile_uni_id=uni.id)
    
    await state.clear()
    
    user_search_settings = await get_search_settings_card(telegram_id=callback.from_user.id)
        
    await callback.message.edit_text(user_search_settings['description'], reply_markup=await get_search_settings_btns(telegram_id=callback.from_user.id))
    
    
    
# ---------------------------------------------- TOPIC ----------------------------------------------

@base_search_settings_profile_router.callback_query(StateFilter(None), F.data.contains("edit_filter_profile_topic"))
async def edit_search_setting_profile(callback: CallbackQuery, state: FSMContext):
    
    await state.update_data(user_id=int(callback.data.split('_')[-1]))
    
    await state.set_state(EditSearchSettingsProfileTopic.topic)
    await callback.answer()
    await callback.message.edit_text("Выберите сферу", reply_markup=await get_topic_btns_for_search_settings())
    
    

@base_search_settings_profile_router.callback_query(StateFilter(EditSearchSettingsProfileTopic.topic), F.data)
async def edit_search_setting_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer(callback.data)
    data = await state.get_data()
    
    filter = await FilterRepository.get_one_or_none(user_id=data['user_id'])
    
    if callback.data == "reset_topic_profile_search_settings":
        topic = None
    else:
        topic = callback.data
        
    await FilterRepository.update(model_id=filter.id, profile_topic=topic)
    await state.clear()
    
    user_search_settings = await get_search_settings_card(telegram_id=callback.from_user.id)
    await callback.message.edit_text(user_search_settings['description'], reply_markup=await get_search_settings_btns(telegram_id=callback.from_user.id))