from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.project import Project

class ProjectRepository(CRUDBase):
    model = Project