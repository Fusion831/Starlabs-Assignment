from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

if TYPE_CHECKING:
    from app.models.booking import Booking

class FitnessClass(Base):
    __tablename__ = "fitness_classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    instructor: Mapped[str] = mapped_column(String(100), nullable=False)
    available_slots: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    bookings: Mapped[List["Booking"]] = relationship(
        "Booking",
        back_populates="fitness_class",
        cascade="all, delete-orphan"
    )
