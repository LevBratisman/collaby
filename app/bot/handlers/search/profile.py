from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from app.common.repository.filter_repository import FilterRepository
from app.common.repository.user_repository import UserRepository
from app.bot.utils.search import transform_filter_for_search_people
from app.bot.keyboards.reply.base import get_keyboard
from app.bot.keyboards.inline.base import get_callback_btns
from app.bot.keyboards.inline.card import get_profile_search_btns
from app.bot.utils.card_generator import get_profile_card


search_profile_router = Router()

@search_profile_router.message(StateFilter(None), F.text.in_(["Следующий", "🔍Искать людей"]))
async def start_search_profile(message: Message):
            
        user = await UserRepository.get_by_telegram_id(telegram_id=message.from_user.id)
        user_filter = await FilterRepository.get_filter_by_telegram_id(telegram_id=message.from_user.id)
        print(user_filter)
        
        if user_filter:
            user_filter = await transform_filter_for_search_people(user_filter) 
            
        
        target_users = await UserRepository.get_users_by_filter(user_id=user.id, **user_filter)
        
        if target_users:
            iter = user.person_iter
            await message.answer("🔍", reply_markup=await get_keyboard("Назад", "Следующий"))
            try:
                await UserRepository.set_person_iterator(message.from_user.id, iter + 1)
                user_description = await get_profile_card(target_users[0][iter].telegram_id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_profile_search_btns(target_users[0][iter].id))
            except IndexError:
                await UserRepository.set_person_iterator(message.from_user.id, 0)
                iter = 0
                user_description = await get_profile_card(target_users[0][iter].telegram_id)
                await message.answer_photo(user_description['photo'],
                                           caption=user_description['description'],
                                           reply_markup=await get_profile_search_btns(target_users[0][iter].id))
        else:
            await message.answer("По вашему запросу ничего не найдено")
        


# @search_people_router.callback_query(StateFilter(None), F.data.startswith('invite_user_'))
# async def invite_user(callback: CallbackQuery, state: FSMContext, bot: Bot):
#     target_user_id = int(callback.data.split('_')[-1])
#     target_user = await UserDAO().get_one_or_none(User.id == target_user_id)
#     inviter = await UserDAO().get_user_by_user_id(callback.from_user.id)
#     if target_user["is_authorized"]:
#         existed_project = await ProjectDAO().get_one_or_none(Project.creator_id == inviter.id)
#         if existed_project:
#             is_already_invited = await RequestDAO().get_one_or_none(Request.project_id == existed_project["id"], Request.user_id == target_user_id)
#             if not is_already_invited:
#                 await RequestDAO().add_one(to_project=False, user_id=target_user_id, project_id=existed_project["id"])
#                 await callback.answer("Приглашение отправлено!")
#                 await bot.send_message(target_user.user_id, f'Вас пригласили в проект!')
#                 return
#             else:
#                 await callback.answer("Вы уже пригласили этого пользователя")
#         else:
#             await callback.answer("Вы еще не опубликовали проект")
#     else:
#         await callback.answer("Этот пользователь удалил свою анкету")