#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from models.place import place_amenity
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    amenity table
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
        "Place", secondary=place_amenity, viewonly=False, back_populates="amenities") \
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
