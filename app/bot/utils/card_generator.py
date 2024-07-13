from app.common.repository.user_repository import UserRepository
from app.common.repository.project_repository import ProjectRepository


async def get_profile_card(telegram_id: int):
    user = await UserRepository.get_card_info_by_telegram_id(telegram_id=telegram_id)
            
    description = f"Имя: {user.name}\nУниверситет: {user.short_name}\nСфера деятельности: {user.topic}\nСтатус аккаунта: {'Premium' if user.is_premium else 'Обычный'}\n\nО себе: {user.info}\n\nНавыки: {user.skills}"
    
    return {'description': description, 'photo': user.image}


async def get_project_card(project_id: int):
    project = await ProjectRepository.get_one_or_none(id=project_id)
    
    description = f"Название: {project.name}\nСфера деятельности: {project.topic}\n\nО проекте: {project.info}\n\nТребования: {project.requirements}"
    
    return {'description': description, 'photo': project.image}


async def get_project_card_with_creator(project_id: int):
    project = await ProjectRepository.get_one_or_none(id=project_id)
    user = await UserRepository.get_by_id(user_id=project.user_id)
    
    if not user:
        return
    
    description = f"Для связи: {user.username}\n\nНазвание: {project.name}\nСфера деятельности: {project.topic}\n\nО проекте: {project.info}\n\nТребования: {project.requirements}"
    
    return {'description': description, 'photo': project.image}