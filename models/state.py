#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="delete", back_populates="state")

    @property
    def cities(self):
        """
        cities getter
        """
        from models import storage
        from models.city import City
        cities = list(
            map(lambda i: i[0],
                filter(lambda i: i.state_id ==
                       self.id, storage.all(City).items())
                )
        )
        return cities
