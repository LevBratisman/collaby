from aiogram.types import InputMediaPhoto

from app.bot.utils.paginator import Paginator
from app.common.models.project import Project
from app.common.models.invite import Invite
from app.common.models.request import Request
from app.bot.utils.card_generator import get_project_card, get_invite_card, get_request_card
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


async def get_invite_kb(invites: list[Invite], page: int = 1):
    try:
        paginator = Paginator(invites, page=page)
        invite = paginator.get_page()[0]
    except IndexError:
        paginator = Paginator(invites, page=1)
        invite = paginator.get_page()[0]
        
    invite_info = await get_invite_card(invite)
        
    image = InputMediaPhoto(media=invite_info['photo'],
                            caption=invite_info['description'])

    pagination_btns = pages(paginator)

    kbds = get_invite_btns(
        page=page,
        pagination_btns=pagination_btns,
        invite_id=invite.id,
    )

    return image, kbds


async def get_request_kb(requests: list[Request], page: int):
    try:
        paginator = Paginator(requests, page=page)
        request = paginator.get_page()[0]
    except IndexError:
        paginator = Paginator(requests, page=1)
        request = paginator.get_page()[0]
        
    request_info = await get_request_card(request)
        
    image = InputMediaPhoto(media=request_info['photo'],
                            caption=request_info['description'])

    pagination_btns = pages(paginator)

    kbds = get_request_btns(
        page=page,
        pagination_btns=pagination_btns,
        request_id=request.id,
    )

    return image, kbds