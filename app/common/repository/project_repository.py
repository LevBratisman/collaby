from sqlalchemy import select

from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.project import Project
from app.db.session import async_session_maker

class ProjectRepository(CRUDBase):
    model = Project
    
    @classmethod
    async def get_projects_by_filter(cls, user_id: int, **filter_data) -> list[Project]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_data).where(cls.model.user_id != user_id)
            result = await session.execute(query)
            return result.scalars().all()
        

    @classmethod
    async def get_claims_projects(cls):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.claim_count>0, cls.model.is_banned==False)
            result = await session.execute(query)
            return result.scalars().all()