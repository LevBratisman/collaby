from sqlalchemy import Integer, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from app.db.base_class import Base, UpdatedModel, CreatedModel

class Premium(Base, CreatedModel, UpdatedModel):
    __tablename__ = "premium"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    
    term: Mapped[int] = mapped_column(Integer)
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)