from sqlalchemy import Column, Integer, ForeignKey, DateTime, event
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from database import Base

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="bookings")
    resource = relationship("Resource", back_populates="bookings")

    @validates('start_time', 'end_time')
    def validate_time(self, key, value):
        if key == 'end_time' and self.start_time and value <= self.start_time:
            raise ValueError("End time must be after start time")
        return value
    

