from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.data.topic_data import topic_data


async def get_topic_btns():
    
    keyboard = InlineKeyboardBuilder()
    
    for key, value in topic_data.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=value))
    
    return keyboard.adjust(2).as_markup()


async def get_topic_btns_for_search_settings():
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text='Сбросить', callback_data='reset_topic_profile_search_settings'))
    
    for key, value in topic_data.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=value))
    
    return keyboard.adjust(1, 2).as_markup()