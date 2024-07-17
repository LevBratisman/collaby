from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

# --------------------- CallBackData --------------------------

class ProjectCallBack(CallbackData, prefix="project"):
    page: int = 1
    project_id: int | None = None
    action: str | None = None

class InviteCallBack(CallbackData, prefix="invite"):
    page: int = 1
    invite_id: int | None = None
    action: str | None = None
    
class RequestCallBack(CallbackData, prefix="request"):
    page: int = 1
    request_id: int | None = None
    action: str | None = None


# --------------------- Get btns for pagination --------------------------

def get_project_btns(
    *,
    page: int,
    pagination_btns: dict,
    project_id: int,
    sizes: tuple[int] = (1, 1, 2)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Удалить',
                callback_data=ProjectCallBack(project_id=project_id, page=page, action="delete").pack()))
    
    keyboard.add(InlineKeyboardButton(text='Заполнить заново',
                callback_data=ProjectCallBack(project_id=project_id, page=page, action="refill").pack()))

    for text, action in pagination_btns.items():
        if action == "next":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=ProjectCallBack(
                        action="next",
                        page=page + 1).pack()))
        
        elif action == "previous":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=ProjectCallBack(
                        action="previous",
                        page=page - 1).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_invite_btns(
    *,
    page: int,
    pagination_btns: dict,
    invite_id: int,
    sizes: tuple[int] = (1, 2)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Удалить',
                callback_data=InviteCallBack(invite_id=invite_id, page=page, action="delete").pack()))

    for text, action in pagination_btns.items():
        if action == "next":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=InviteCallBack(
                        action="next",
                        page=page + 1).pack()))
        
        elif action == "previous":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=InviteCallBack(
                        action="previous",
                        page=page - 1).pack()))

    return keyboard.adjust(*sizes).as_markup()



def get_request_btns(
    *,
    page: int,
    pagination_btns: dict,
    request_id: int,
    sizes: tuple[int] = (1, 2)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Удалить',
                callback_data=RequestCallBack(request_id=request_id, page=page, action="delete").pack()))

    for text, action in pagination_btns.items():
        if action == "next":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=RequestCallBack(
                        action="next",
                        page=page + 1).pack()))
        
        elif action == "previous":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=RequestCallBack(
                        action="previous",
                        page=page - 1).pack()))

    return keyboard.adjust(*sizes).as_markup()