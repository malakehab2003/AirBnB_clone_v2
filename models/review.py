#!/usr/bin/python3
""" Review module for the HBNB project """
import os
from sqlalchemy import Column, ForeignKey, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = "reviews"
    place = relationship("Place")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    user = relationship("User")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    text = Column(String(1024), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
