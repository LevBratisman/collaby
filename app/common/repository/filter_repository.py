from sqlalchemy import select

from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.filter import Filter
from app.db.session import async_session_maker

class FilterRepository(CRUDBase):
    model = Filter
    
    @classmethod
    async def get_filter_by_telegram_id(cls, telegram_id: int) -> dict:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).where(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()