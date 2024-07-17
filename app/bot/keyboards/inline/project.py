from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


from app.common.models.project import Project


# --------------------- CallBackData --------------------------

class InviteUserCallBack(CallbackData, prefix="invite_user"):
    project_id: int | None = None
    target_user_id: int | None = None
    sender_user_id: int | None = None
    action: str | None = None
    

class RequestProjectCallBack(CallbackData, prefix="request_project"):
    target_project_id: int | None = None
    user_id: int | None = None
    sender_user_id: int | None = None
    action: str | None = None


async def get_projects(projects: list[Project], target_user_id: int, sender_user_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="<< Назад", callback_data=InviteUserCallBack(target_user_id=target_user_id, action="cancel").pack()))
    
    for project in projects:
        keyboard.add(InlineKeyboardButton(text=project.name, callback_data=InviteUserCallBack(target_user_id=target_user_id, project_id=project.id, sender_user_id=sender_user_id, action="invite").pack()))
        
    return keyboard.adjust(1, 2).as_markup()