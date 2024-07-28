from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.common.repository.filter_repository import FilterRepository

async def get_profile_btns(user_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    btns = {
        "Удалить анкету": f"delete_profile_{user_id}",
        "Заполнить заново": f"refill_profile_{user_id}"
    }
    
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    
    return keyboard.as_markup()


async def get_profile_delete_btns(user_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    btns = {
        "Подтвердить": f"delete_profile_{user_id}",
        "Отменить": f"cancel_delete_profile_{user_id}"
    }
    
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    
    return keyboard.as_markup()


async def get_profile_search_btns(user_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    btns = {
        "Пригласить": f"invite_profile_{user_id}",
        "Пожаловаться": f"report_profile_{user_id}"
    }
    
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    
    return keyboard.adjust(1, 1).as_markup()


async def get_project_search_btns(project_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    btns = {
        "Подать заявку": f"request_project_{project_id}",
        "Пожаловаться": f"report_project_{project_id}"
    }
    
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    
    return keyboard.adjust(1, 1).as_markup()


async def get_search_settings_btns(telegram_id: int):
    
    filter = await FilterRepository.get_one_or_none(telegram_id=telegram_id)
    
    keyboard = InlineKeyboardBuilder()
    
    btns = {
        "Универ (профили)": f"edit_filter_profile_uni_{filter.user_id}",
        "Универ (проекты)": f"edit_filter_project_uni_{filter.user_id}",
        "Сфера (профили)": f"edit_filter_profile_topic_{filter.user_id}",
        "Сфера (проекты)": f"edit_filter_project_topic_{filter.user_id}"
    }
    
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    
    return keyboard.adjust(2, 2).as_markup()