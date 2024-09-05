from aiogram import Router
from aiogram.types import Message

base_router = Router()

@base_router.message()
async def handle_unknown_message(message: Message):
    await message.answer("Неизвестная команда")