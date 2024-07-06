from sqlalchemy import select

from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.user import User
from app.db.session import async_session_maker

class UserRepository(CRUDBase):
    model = User
    
    @classmethod
    async def get_by_telegram_id(cls, telegram_id: int) -> User | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()