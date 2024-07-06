from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.filter import Filter

class FilterRepository(CRUDBase):
    model = Filter