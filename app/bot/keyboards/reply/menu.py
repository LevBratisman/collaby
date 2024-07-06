from aiogram.types import ReplyKeyboardMarkup
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
    sizes: tuple[int] = (2, 2, 2, 1,),
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
    )
    
    keyboard = ReplyKeyboardBuilder()
    
    user = await UserRepository.get_by_telegram_id(telegram_id=telegram_id)
    requests_invites_info = await get_invites_requests_info(telegram_id=telegram_id)
    
    for index, text in enumerate(btns, start=0):
        
        if request_contact is not None and index == request_contact:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
            
        elif request_location is not None and index == request_location:
            keyboard.add(KeyboardButton(text=text, request_location=True))
            
        else:
            if index == 2 and requests:
                keyboard.add(KeyboardButton(text=text + f" ({len(requests)})"))
            elif index == 3 and invites:
                keyboard.add(KeyboardButton(text=text + f" ({len(invites)})"))
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
    # requests = await RequestRepository.get_all(project_id=Request.project.user_iadapt_to_entity)
    
    