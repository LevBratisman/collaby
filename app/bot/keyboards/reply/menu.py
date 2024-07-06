from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.common.repository.user_repository import UserRepository
from app.common.repository.invite_repository import InviteRepository
from app.common.repository.request_repository import RequestRepository
from app.common.models.user import User
from app.common.models.request import Request


async def get_menu_keyboard(
    placeholder: str = "Выберите действие",
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2, 2, 2, 1, 1,),
    telegram_id: int = None
) -> ReplyKeyboardMarkup:
    
    btns = (
        "🔍Искать людей",
        "💡Искать проекты",
        "🙋🏻‍♂️Заявки",
        "🔔Приглашения",
        "🎴Мой профиль",
        "👥Мои проекты",
        "⚙️Параметры поиска",
        "💎Premium"
    )
    
    keyboard = ReplyKeyboardBuilder()
    
    user = await UserRepository.get_by_telegram_id(telegram_id=telegram_id)
    requests_invites_info = await get_invites_requests_info(user=user)
    
    for index, text in enumerate(btns, start=0):
        if index == 2:
            if requests_invites_info['requests'] > 0:
                keyboard.add(KeyboardButton(text=f"{text} ({requests_invites_info['requests']})"))
            else:
                keyboard.add(KeyboardButton(text=text))
        elif index == 3:
            if requests_invites_info['invites'] > 0:
                keyboard.add(KeyboardButton(text=f"{text} ({requests_invites_info['invites']})"))
            else:
                keyboard.add(KeyboardButton(text=text))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )
    
    
async def get_invites_requests_info(user: User) -> dict:
    
    info = {
        "requests": 0,
        "invites": 0
    }
    
    invites = await InviteRepository.get_all(user_id=user.id)
    requests = await RequestRepository.get_request_project_info(user_id=user.id)
    
    info["requests"] = len(requests)
    info["invites"] = len(invites)
    
    return info
    
    