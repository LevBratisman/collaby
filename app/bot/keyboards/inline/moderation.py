from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.bot.data.report_reason_data import report_reason_data, moderate_data

class ModerationCallBackUser(CallbackData, prefix="ban_user"):
    to_project: bool
    target_id: int


class ModerationCallBackProject(CallbackData, prefix="ban_project"):
    to_project: bool
    target_id: int


async def get_moderate_kb_for_users(target_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    
    for key, value in moderate_data.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=ModerationCallBackUser(target_id=target_id, to_project=False).pack()))
        
    return keyboard.adjust(1).as_markup()


async def get_moderate_kb_for_projects(target_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    
    for key, value in moderate_data.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=ModerationCallBackProject(target_id=target_id, to_project=True).pack()))
        
    return keyboard.adjust(1).as_markup()