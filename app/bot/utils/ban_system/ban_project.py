import datetime

from app.common.repository.invite_repository import InviteRepository
from app.common.repository.report_repository import ReportRepository
from app.common.repository.user_repository import UserRepository
from app.common.repository.request_repository import RequestRepository
from app.common.repository.project_repository import ProjectRepository

from app.common.models.project import Project

from app.bot.utils.ban_system.ban_profile import ban_profile


async def ban_project(project: Project):
    
    await ReportRepository.delete_by(project_id=project.id)
    await RequestRepository.delete_by(project_id=project.id)
    await InviteRepository.delete_by(project_id=project.id)
    await ProjectRepository.delete(model_id=project.id)

    user = await UserRepository.get_by_id(model_id=project.user_id)
    
    await UserRepository.update(model_id=project.user_id, claim_count=user.claim_count + 1)
    
    if user.claim_count == 10:
        await ban_profile(user)
    
