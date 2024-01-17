#!/usr/bin/python3
"""This module defines a class User"""
import os
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = "users"
    email = Column(String(128), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    password = Column(String(128), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    first_name = Column(String(128))\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    last_name = Column(String(128))\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    places = relationship("Place", cascade="delete", back_populates="user")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    reviews = relationship("Review", cascade="delete", back_populates="user")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
