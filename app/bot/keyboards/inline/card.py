from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.common.models.user import User


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