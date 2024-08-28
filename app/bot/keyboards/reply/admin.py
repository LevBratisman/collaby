from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Создание reply кнопок
async def get_admin_keyboard():
    
    btns = [
        "Модерация пользователей",
        "Модерация проектов",
        "Добавить бота",
        "Добавить проект",
        "Статистика",
        "Назад"
    ]
    
    keyboard = ReplyKeyboardBuilder()
    
    for index, text in enumerate(btns, start=0):
            keyboard.add(KeyboardButton(text=text))
            
    return keyboard.adjust(2, 2, 1, 1).as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите действие'
    )