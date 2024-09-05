from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.common.repository.uni_repository import UniRepository


async def get_uni_btns():
    
    keyboard = InlineKeyboardBuilder()
    unis = await UniRepository.get_all()
    
    for uni in unis:
        keyboard.add(InlineKeyboardButton(text=uni.short_name, callback_data=uni.short_name))
    
    return keyboard.adjust(2).as_markup()