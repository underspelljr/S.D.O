from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db.base import BaseIdUuid
from typing import List

class User(BaseIdUuid):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, index=True, unique=True)
    
    spots: Mapped[List["Spot"]] = relationship("Spot", back_populates="created_by")