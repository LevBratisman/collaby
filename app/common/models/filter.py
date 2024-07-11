from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, CreatedModel

class Filter(Base, CreatedModel):
    __tablename__ = "filter"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    
    project_uni_id: Mapped[int] = mapped_column(ForeignKey("uni.id"), nullable=True)
    project_topic: Mapped[str] = mapped_column(String(30), nullable=True)
    
    profile_uni_id: Mapped[int] = mapped_column(ForeignKey("uni.id"), nullable=True)
    profile_topic: Mapped[str] = mapped_column(String(30), nullable=True)
    
    profile_uni = relationship("Uni", foreign_keys=[profile_uni_id])
    project_uni = relationship("Uni", foreign_keys=[project_uni_id])
    
    