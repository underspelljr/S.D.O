from sqlalchemy import String, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseId
from typing import Optional


class Spot(BaseId):
    __tablename__ = "spots"

    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_by: Mapped["User"] = relationship("User", back_populates="spots")
