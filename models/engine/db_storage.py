#!/usr/bin/python3
"""This module defines a class to manage sql storage for hbnb clone"""
from sqlalchemy import (asc, create_engine, MetaData)
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base, BaseModel
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in SQL"""

    __engine = None
    __session = None

    classes = {
        "City": City, "User": User, "State": State,
        "Amenity": Amenity, "Place": Place, "Review": Review
    }

    def __init__(self):
        user = os.environ.get("HBNB_MYSQL_USER")
        password = os.environ.get("HBNB_MYSQL_PWD")
        host = os.environ.get("HBNB_MYSQL_HOST")
        database = os.environ.get("HBNB_MYSQL_DB")
        env = os.environ.get("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, database), pool_pre_ping=True)
        if env == "test":
            md = MetaData()
            md.reflect(bind=self.__engine)
            md.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        query on the current database session
        """
        if cls is not None:
            if type(cls) is not str:
                cls = cls.__name__
            rows = self.__session.query(self.classes[cls]).all()
        else:
            rows = []
            for cls in self.classes.values():
                rows.extend(self.__session.query(cls).all())
        result = {}
        for row in rows:
            key = cls+"."+row.id
            result[key] = row
        return result

    def new(self, obj):
        """
        add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session
        """
        self.__session.delete(obj)

    def reload(self):
        """
        reload session connection
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False, )
        self.__session = scoped_session(Session)
