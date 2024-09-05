from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True
)

async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False, 
    autoflush=False
)