from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base_class import Base, CreatedModel

class BannedUser(Base, CreatedModel):
    __tablename__ = "banned_user"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    term: Mapped[int] = mapped_column(Integer)
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", foreign_keys=[user_id])