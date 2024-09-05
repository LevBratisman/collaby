from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command

from app.bot.keyboards.reply.menu import get_menu_keyboard


from app.bot.text.common import premium_text

base_premium_router = Router()

@base_premium_router.message(StateFilter('*'), F.text == "💎Premium")
async def premium(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(premium_text, reply_markup=await get_menu_keyboard(telegram_id=message.from_user.id))
    
