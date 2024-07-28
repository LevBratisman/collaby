from datetime import datetime

from app.common.repository.project_repository import ProjectRepository
from app.common.repository.banned_project_repository import BannedProjectRepository

from app.common.models.project import Project
from app.common.models.user import User


async def ban_project(project: Project, user: User):
    await ProjectRepository().update(model_id=project.id, is_banned=True)
    
    term_days = 10
    date_end = datetime.now() + datetime.timedelta(days=term_days)
    
    await BannedProjectRepository().add(project_id=project.id, user_id=user.id, term=term_days, date_end=date_end)
    
    
async def unban_project(project: Project):
    await ProjectRepository().update(model_id=project.id, is_banned=False)
    await BannedProjectRepository().delete(project_id=project.id)