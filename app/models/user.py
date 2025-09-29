from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db.base import BaseIdUuid
from typing import List

class User(BaseIdUuid):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, index=True, unique=True)
    permission_level: Mapped[int] = mapped_column(default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    spots: Mapped[List["Spot"]] = relationship("Spot", back_populates="created_by")