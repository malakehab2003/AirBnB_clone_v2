#!/usr/bin/python3
""" City Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    state = relationship("State")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    places = relationship("Place", cascade="delete", back_populates="cities")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
