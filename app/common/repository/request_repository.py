from sqlalchemy import select, join

from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.request import Request
from app.common.models.project import Project
from app.db.session import async_session_maker

class RequestRepository(CRUDBase):
    model = Request
    
    @classmethod
    async def get_request_project_info(cls, user_id: int) -> dict:
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns
            ).join(Project).filter(
                cls.model.project_id == Project.id
            ).where(
                Project.user_id == user_id
            )
            
            result = await session.execute(query)
            return result.all()