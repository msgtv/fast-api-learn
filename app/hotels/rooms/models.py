from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(ForeignKey('hotels.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    hotel = relationship("Hotels", back_populates="rooms")

    def __str__(self):
        return f"Room #{self.id}"
