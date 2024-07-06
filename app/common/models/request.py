from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, CreatedModel

class Request(Base, CreatedModel):
    __tablename__ = "request"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    
    message: Mapped[str] = mapped_column(String(500), nullable=True)
    
    user = relationship("User", foreign_keys=[user_id])
    project = relationship("Project", foreign_keys=[project_id])