#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


place_amenity = Table("place_amenity",
                      Base.metadata,
                      Column("place_id", String(60), ForeignKey(
                          "places.id"), primary_key=True, nullable=False),
                      Column("amenity_id", String(60), ForeignKey(
                          "amenities.id"), primary_key=True,
                          nullable=False),
                      ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    cities = relationship("City") \
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    user = relationship("User")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    name = Column(String(128), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    description = Column(String(1024))\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    number_rooms = Column(Integer(), nullable=False, default=0)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    number_bathrooms = Column(Integer(), nullable=False, default=0)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    max_guest = Column(Integer(), nullable=False, default=0)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    price_by_night = Column(Integer(), nullable=False, default=0)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    latitude = Column(Float())\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    longitude = Column(Float())\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    reviews = relationship("Review", cascade="delete", back_populates="place")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            "Amenity", secondary=place_amenity, viewonly=False,
            back_populates="place_amenities")
    else:
        @property
        def amenities(self):
            """
            for FileStorage: getter attribute amenities
            """
            from models import storage
            from models.amenity import Amenity
            amenities = list(
                map(lambda i: i[0],
                    filter(lambda i: i.id in
                           self.amenity_ids, storage.all(Amenity).values())
                    )
            )
            return amenities

        @amenities.setter
        def amenities(self, amenity):
            """
            Setter attribute amenities
            """
            from models.amenity import Amenity
            print("appending")
            if type(amenity) is Amenity:
                self.amenity_ids.append(amenity.id)

    amenity_ids = []
    if os.getenv('HBNB_TYPE_STORAGE') is None \
            or os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """
            for FileStorage: getter attribute reviews
            """
            from models import storage
            from models.review import Review
            reviews = list(
                map(lambda i: i[0],
                    filter(lambda i: i.place_id ==
                           self.id, storage.all(Review).values())
                    )
            )
            return reviews
