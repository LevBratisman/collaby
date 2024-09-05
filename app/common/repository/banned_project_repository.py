from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.banned_project import BannedProject

class BannedProjectRepository(CRUDBase):
    model = BannedProject