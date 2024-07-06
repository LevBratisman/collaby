from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class Uni(Base):
    __tablename__ = "uni"
        
    full_name: Mapped[str] = mapped_column(String(100))
    short_name: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    city: Mapped[str] = mapped_column(String(30))