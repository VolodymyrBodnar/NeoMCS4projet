from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from ..database import Base
from .booking import Booking


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    bookings = relationship(Booking, back_populates="resource")

    @validates("description")
    def validate_description(self, key, value):
        if key == "description" and value:
            if len(value) < 5:
                raise ValueError("Tooo short")
            elif len(value) > 155:
                raise ValueError("Too loong")
        return value
