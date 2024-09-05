from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, CreatedModel

class Report(Base, CreatedModel):
    __tablename__ = "report"
    
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=True)
    
    to_project: Mapped[bool] = mapped_column(default=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=True)
    
    user = relationship("User", foreign_keys=[user_id])
    project = relationship("Project", foreign_keys=[project_id])