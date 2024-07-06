from sqlalchemy import select, update, delete, insert

from app.db.session import async_session_maker
from app.db.base_class import ModelType

class CRUDBase:    
    model = None
    
    @classmethod
    async def get_by_id(cls, model_id: int) -> ModelType | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.id == model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()
    
    @classmethod
    async def get_one_or_none(cls, **filters) -> ModelType | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().one_or_none()
    
    @classmethod
    async def get_all(cls, **filters) -> list[ModelType] | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            
    @classmethod
    async def delete(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.id == model_id)
            result = await session.execute(query)
            if not result:
                raise Exception
            else:
                query = delete(cls.model).where(cls.model.id == model_id)
                await session.execute(query)
                await session.commit()
                
    @classmethod
    async def update(cls, model_id: int, **data):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.id == model_id)
            result = await session.execute(query)
            if not result:
                raise Exception
            else:
                query = update(cls.model).where(cls.model.id == model_id).values(**data)
                await session.execute(query)
                await session.commit()
            