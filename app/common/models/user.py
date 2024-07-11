from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, UpdatedModel, CreatedModel

class User(Base, CreatedModel, UpdatedModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(30), unique=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    info: Mapped[str] = mapped_column(String(700), nullable=True)
    skills: Mapped[str] = mapped_column(String(700), nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    topic: Mapped[str] = mapped_column(String(30), index=True, nullable=True)
    uni_id: Mapped[int] = mapped_column(ForeignKey("uni.id"))
    claim_count: Mapped[int] = mapped_column(default=0)
    
    is_banned: Mapped[bool] = mapped_column(default=False)
    is_authorized: Mapped[bool] = mapped_column(default=False)
    is_premium: Mapped[bool] = mapped_column(default=False)
    
    person_iter: Mapped[int] = mapped_column(default=0)
    project_iter: Mapped[int] = mapped_column(default=0)
    
    uni = relationship("Uni", backref="users")
    