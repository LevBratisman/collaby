from sqlalchemy import select, join, outerjoin, update

from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.user import User
from app.common.models.uni import Uni
from app.common.models.filter import Filter
from app.common.models.premium import Premium
from app.db.session import async_session_maker

class UserRepository(CRUDBase):
    model = User
    
    @classmethod
    async def get_by_telegram_id(cls, telegram_id: int) -> User | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.one_or_none()
        
    @classmethod
    async def get_full_info_by_telegram_id(cls, telegram_id: int) -> User | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns, Uni.__table__.columns, Filter.__table__.columns
                            ).join(Filter, cls.model.id == Filter.user_id
                            ).join(Uni, cls.model.uni_id == Uni.id
                            ).filter(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.one_or_none()
        
    @classmethod
    async def get_card_info_by_telegram_id(cls, telegram_id: int) -> User | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns, Uni.short_name, Premium.date_end
                            ).join(Uni, cls.model.uni_id == Uni.id
                            ).outerjoin(Premium, cls.model.id == Premium.user_id
                            ).filter(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.one_or_none()
        
        
    @classmethod
    async def get_users_by_filter(cls, user_id: int, **filter_data) -> list[User]:
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.all()
        
        
    # ITERATORS
    
    @classmethod
    async def set_person_iterator(cls, telegram_id: int, value: int):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.telegram_id == telegram_id).values(person_iter = value)
            await session.execute(query)
            await session.commit()
            
            
    @classmethod
    async def set_project_iterator(cls, telegram_id: int, value: int):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.telegram_id == telegram_id).values(project_iter = value)
            await session.execute(query)
            await session.commit()