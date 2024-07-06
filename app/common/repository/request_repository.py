from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.request import Request

class RequestRepository(CRUDBase):
    model = Request