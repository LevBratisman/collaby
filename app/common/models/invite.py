from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, CreatedModel

class Invite(Base, CreatedModel):
    __tablename__ = "invite"
    
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    message: Mapped[str] = mapped_column(String(500), nullable=True)
    
    project = relationship("Project", foreign_keys=[project_id])
    sender = relationship("User", foreign_keys=[sender_id])