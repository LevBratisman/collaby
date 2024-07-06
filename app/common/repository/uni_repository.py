from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.uni import Uni

class UniRepository(CRUDBase):
    model = Uni