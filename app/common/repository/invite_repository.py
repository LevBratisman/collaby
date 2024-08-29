from sqlalchemy import select
from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.invite import Invite
from app.common.models.project import Project
from app.db.session import async_session_maker

class InviteRepository(CRUDBase):
    model = Invite

    @classmethod
    async def get_invite_project_info(cls, user_id: int) -> dict:
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns
            ).where(
                cls.model.user_id == user_id
            )
            
            result = await session.execute(query)
            return result.all()  