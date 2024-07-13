from aiogram.types import InputMediaPhoto

from app.bot.utils.paginator import Paginator
from app.common.models.project import Project
from app.bot.utils.card_generator import get_project_card
from app.bot.keyboards.inline.pagination import get_project_btns, get_invite_btns, get_request_btns


def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns


async def get_project_kb(projects: list[Project], page: int = 1):
    try:
        paginator = Paginator(projects, page=page)
        project = paginator.get_page()[0]
    except IndexError:
        paginator = Paginator(projects, page=1)
        project = paginator.get_page()[0]
        
    project_info = await get_project_card(project.id)
        
    image = InputMediaPhoto(media=project_info['photo'],
                            caption=project_info['description'])

    pagination_btns = pages(paginator)

    kbds = get_project_btns(
        page=page,
        pagination_btns=pagination_btns,
        project_id=project.id,
    )

    return image, kbds


async def get_invites_menu(invites: list[dict], page: int):
    try:
        paginator = Paginator(invites, page=page)
        invite = paginator.get_page()[0]
    except IndexError:
        paginator = Paginator(invites, page=1)
        invite = paginator.get_page()[0]
    
    project = await ProjectDAO().get_one_or_none(Project.id == invite['project_id'])
    
    if project:
        image = InputMediaPhoto(media=project['photo'],
                                caption=await get_project_full_info_with_creator(project))
        
    pagination_btns = pages(paginator)
    
    kbds = get_invite_btns(
        page=page,
        pagination_btns=pagination_btns,
        invite_id=invite['id'],
    )

    return image, kbds


async def get_requests_menu(requests: list[dict], page: int):
    try:
        paginator = Paginator(requests, page=page)
        request = paginator.get_page()[0]
    except IndexError:
        paginator = Paginator(requests, page=1)
        request = paginator.get_page()[0]
    
    user = await UserDAO().get_one_or_none(User.id == request['user_id'])
    
    if user:
        card = await get_user_card_with_username(user['user_id'])
        image = InputMediaPhoto(media=user['photo'],
                                caption=card['description'])
        
    pagination_btns = pages(paginator)
    
    kbds = get_request_btns(
        page=page,
        pagination_btns=pagination_btns,
        request_id=request['id'],
    )

    return image, kbds