import datetime

from app.common.repository.invite_repository import InviteRepository
from app.common.repository.report_repository import ReportRepository
from app.common.repository.request_repository import RequestRepository
from app.common.repository.user_repository import UserRepository
from app.common.repository.banned_user_repository import BannedUserRepository
from app.common.repository.project_repository import ProjectRepository

from app.common.models.user import User

async def ban_profile(user: User):
    await UserRepository.update(model_id=user.id, is_banned=True)
    
    term_days = 7
    date_end = datetime.datetime.now() + datetime.timedelta(days=term_days)
    
    await BannedUserRepository.add(user_id=user.id, term=term_days, date_end=date_end)
    projects = await ProjectRepository.get_all(user_id=user.id)

    for project in projects:
        await ReportRepository.delete_by(project_id=project.id)
        await RequestRepository.delete_by(project_id=project.id)
        await InviteRepository.delete_by(project_id=project.id)
        await ProjectRepository.delete(model_id=project.id)
    
    
async def unban_profile(user: User):
    await UserRepository.update(model_id=user.id, is_banned=False, claim_count=0)
    await BannedUserRepository.delete_by(user_id=user.id)