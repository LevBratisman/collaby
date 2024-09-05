from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.report import Report

class ReportRepository(CRUDBase):
    model = Report