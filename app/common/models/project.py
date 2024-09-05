from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, UpdatedModel, CreatedModel

class Project(Base, CreatedModel, UpdatedModel):
    __tablename__ = "project"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    uni_id: Mapped[int] = mapped_column(ForeignKey("uni.id"))
    
    name: Mapped[str] = mapped_column(String(30))
    info: Mapped[str] = mapped_column(String(1000))
    requirements: Mapped[str] = mapped_column(String(1000))
    image: Mapped[str] = mapped_column(nullable=True)
    topic: Mapped[str] = mapped_column(String(30), index=True)
    claim_count: Mapped[int] = mapped_column(default=0)
    
    is_banned: Mapped[bool] = mapped_column(default=False)
    
    user = relationship("User", backref="projects")
    uni = relationship("Uni", backref="projects")