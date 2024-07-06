from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.banned_user import BannedUser

class BannedUserRepository(CRUDBase):
    model = BannedUser