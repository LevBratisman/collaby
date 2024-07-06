from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base_class import Base, CreatedModel

class BannedProject(Base, CreatedModel):
    __tablename__ = "banned_project"

    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    term: Mapped[int] = mapped_column(Integer)
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    project = relationship("Project", foreign_keys=[project_id])
    user = relationship("User", foreign_keys=[user_id])