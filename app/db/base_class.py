from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.sql import func

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


@declarative_mixin
class CreatedModel:
    """
    An abstract base class model that provides create date information
    ``created_at``
    """

    created_at = Column(DateTime(timezone=True), server_default=func.now())


@declarative_mixin
class UpdatedModel:
    """
    An abstract base class model that provides update date information
    ``updated_at``
    """

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())