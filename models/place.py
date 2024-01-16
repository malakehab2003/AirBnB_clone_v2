#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    cities = relationship("City")
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer(), nullable=False, default=0)
    number_bathrooms = Column(Integer(), nullable=False, default=0)
    max_guest = Column(Integer(), nullable=False, default=0)
    price_by_night = Column(Integer(), nullable=False, default=0)
    latitude = Column(Float())
    longitude = Column(Float())
    reviews = relationship("Review", cascade="delete", back_populates="place")

    @property
    def reviews(self):
        """
        for FileStorage: getter attribute reviews
        """
        from models import storage
        from models.review import Review
        cities = list(
            map(lambda i: i[0],
                filter(lambda i: i.place_id ==
                       self.id, storage.all(Review).items())
                )
        )
        return cities
