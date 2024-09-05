from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.premium import Premium

class PremiumRepository(CRUDBase):
    model = Premium