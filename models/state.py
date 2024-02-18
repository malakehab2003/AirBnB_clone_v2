#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    cities = relationship("City", cascade="delete", back_populates="state")\
        if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """
            cities getter
            """
            from models import storage
            from models.city import City
            cities = list(
                map(lambda i: i,
                    filter(lambda i: i.state_id ==
                           self.id, storage.all(City).values())
                    )
            )
            return cities
