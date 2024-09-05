from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.bot.data.report_reason_data import report_reason_data

class ReportCallBack(CallbackData, prefix="report"):
    to_project: bool
    target_id: int
    sender_id: int
    reason: str | None = None
    action: str


async def get_report_reasons_for_user(sender_id: int, target_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="<< Назад", callback_data=ReportCallBack(target_id=target_id, sender_id=sender_id, to_project=False, action="cancel").pack()))
    
    for key, value in report_reason_data.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=ReportCallBack(reason=value, target_id=target_id, sender_id=sender_id, to_project=False, action="report").pack()))
        
    return keyboard.adjust(1, 2).as_markup()


async def get_report_reasons_for_project(sender_id: int, target_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="<< Назад", callback_data=ReportCallBack(target_id=target_id, sender_id=sender_id, to_project=True, action="cancel").pack()))
    
    for key, value in report_reason_data.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=ReportCallBack(reason=value, target_id=target_id, sender_id=sender_id, to_project=True, action="report").pack()))
        
    return keyboard.adjust(1, 2).as_markup()