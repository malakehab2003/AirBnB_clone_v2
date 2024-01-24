#!/usr/bin/python3
""" """
import os
import unittest
from models.city import City
from models.state import State
from models import storage
import datetime
from models.base_model import BaseModel


class test_City(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.state = State()
        self.state.name = "Testing"
        self.state.save()
        self.name = "City"
        self.value = City()

    def test_state_id(self):
        """ """
        new = self.value
        self.assertEqual(new.state_id, None
                         if os.getenv("HBNB_TYPE_STORAGE") == 'db'
                         else "")

    def test_name(self):
        """ """
        new = self.value
        self.assertEqual(new.name, None
                         if os.getenv("HBNB_TYPE_STORAGE") == 'db'
                         else "")

    def test_city_attributes(self):
        """test atters"""
        city = City()
        self.assertEqual(city.name, None
                         if os.getenv("HBNB_TYPE_STORAGE") == 'db'
                         else "")
        self.assertEqual(city.state_id, None
                         if os.getenv("HBNB_TYPE_STORAGE") == 'db'
                         else "")

    def test_city_inheritance(self):
        """test inheritance"""
        city = City()
        self.assertIsInstance(city, BaseModel)

    def test_created_at(self):
        """test created at"""
        city = City()
        self.assertTrue(type(city.created_at) is datetime.datetime)

    def test_save(self):
        """test save"""
        city = City()
        city.name = "Test"
        city.state_id = self.state.id
        first_date = city.updated_at
        city.save()
        second_date = city.updated_at
        self.assertNotEqual(first_date, second_date)

    def test_save_file(self):
        """test save file"""
        city = City()
        city.name = 'Test'
        city.state_id = self.state.id
        city.save()
        user_id = f"City.{city.id}"
        self.assertIn(user_id, storage.all())
