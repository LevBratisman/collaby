from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.data.topic_data import topic_data


async def get_topic_btns():
    
    keyboard = InlineKeyboardBuilder()
    
    for key, value in topic_data.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=value))
    
    return keyboard.adjust(2).as_markup()