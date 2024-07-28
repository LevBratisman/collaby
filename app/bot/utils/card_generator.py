from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository
from app.common.repository.uni_repository import UniRepository
from app.common.repository.filter_repository import FilterRepository
from app.common.models.invite import Invite
from app.common.models.request import Request

# --------------------- PROFILE ---------------------

async def get_profile_card(telegram_id: int):
    user = await UserRepository.get_card_info_by_telegram_id(telegram_id=telegram_id)
            
    description = f"Имя: {user.name}\nУниверситет: {user.short_name}\nСфера деятельности: {user.topic}\nСтатус аккаунта: {'Premium' if user.is_premium else 'Обычный'}\n\nО себе: {user.info}\n\nНавыки: {user.skills}"
    
    return {'description': description, 'photo': user.image}


# --------------------- PROJECT ---------------------

async def get_project_card(project_id: int):
    project = await ProjectRepository.get_one_or_none(id=project_id)
    
    description = f"Название: {project.name}\nСфера деятельности: {project.topic}\n\nО проекте: {project.info}\n\nТребования: {project.requirements}"
    
    return {'description': description, 'photo': project.image}


# --------------------- INVITE ---------------------

async def get_invite_card(invite: Invite):
    project = await ProjectRepository.get_one_or_none(id=invite.project_id)
    user = await UserRepository.get_by_id(model_id=project.user_id)
    uni = await UniRepository.get_by_id(model_id=project.uni_id)
    
    if not user:
        return
    
    description = f"Для связи: @{user.username}\n\nНазвание: {project.name}\nУниверситет: {uni.short_name}\nСфера деятельности: {project.topic}\n\nО проекте: {project.info}\n\nТребования: {project.requirements}"
    
    return {'description': description, 'photo': project.image}


# --------------------- REQUEST ---------------------

async def get_request_card(request: Request):
    user = await UserRepository.get_by_id(model_id=request.user_id)
    project = await ProjectRepository.get_one_or_none(id=request.project_id)
    uni = await UniRepository.get_by_id(model_id=project.uni_id)
    
    if not user:
        return
    
    description = f"Для связи: @{user.username}\n\nИмя: {user.name}\nУниверситет: {uni.short_name}\nСфера деятельности: {user.topic}\nСтатус аккаунта: {'Premium' if user.is_premium else 'Обычный'}\n\nО себе: {user.info}\n\nНавыки: {user.skills}"
    
    return {'description': description, 'photo': user.image}


# --------------------- SEARCH SETTINGS ---------------------


async def get_search_settings_card(telegram_id: int):
    filter = await FilterRepository.get_one_or_none(telegram_id=telegram_id)
    
    profile_filter_uni = await UniRepository.get_by_id(model_id=filter.profile_uni_id)
    project_filter_uni = await UniRepository.get_by_id(model_id=filter.project_uni_id)
    
    description = f"⚙️ПОИСК ПО ПРОФИЛЯМ⚙️\n\nУниверситет: <b>{profile_filter_uni.short_name}</b>\nСфера: <b>{filter.profile_topic}</b>\n\n\n⚙️ПОИСК ПО ПРОЕКТАМ⚙️\n\nУниверситет: <b>{project_filter_uni.short_name}</b>\nСфера: <b>{filter.project_topic}</b>\n\n{'〰️' * 15}\n\n🔽Изменить параметры🔽"
    
    return {'description': description}


# --------------------- ADMIN STATISTICS ---------------------


async def get_admin_statistics_card():
    users = await UserRepository.get_all()
    projects = await ProjectRepository.get_all()
    authorized_users = len([user for user in users if user.is_authorized])
    banned_users = len([user for user in users if user.is_banned])
    banned_projects = len([project for project in projects if project.is_banned])
    vip_users = len([user for user in users if user.is_premium])
    
    description = f"Кол-во пользователей: {len(users)}\nКол-во проектов: {len(projects)}\nАвторизованныe пользователи: {authorized_users}\nЗабаненные пользователи: {banned_users}\nPremium пользователи: {vip_users}\nЗабанненные проекты: {banned_projects}"
    
    return description