from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.invite import Invite

class InviteRepository(CRUDBase):
    model = Invite