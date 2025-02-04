#!/usr/bin/python3
""" test base model """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ test base model """

    def __init__(self, *args, **kwargs):
        """ make the constructor """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel()

    def tearDown(self):
        """test"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_kwargs(self):
        """test adding kwargs """
        i = self.value
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ test int """
        i = self.value
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "FileStorage Test")
    def test_save(self):
        """ Testing save """
        i = self.value
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(self.name, "BaseModel")
            self.assertEqual(j[key], i.to_dict())

    def test_todict(self):
        """ test_todict """
        i = self.value
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """test_kwargs_none """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        """test_id """
        new = self.value
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """test_created_at """
        new = self.value
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """test_updated_at """
        new = self.value
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "FileStorage Test")
    def test_base(self):
        """
        base test
        """
        my_model = BaseModel()
        self.assertIsInstance(my_model, BaseModel)
        self.assertIsInstance(my_model.id, str)
        self.assertIsInstance(my_model.created_at, datetime.datetime)
        self.assertIsInstance(my_model.updated_at, datetime.datetime)
        my_model.name = "My First Model"
        my_model.my_number = 89
        my_dict = {
            "id": my_model.id,
            'created_at': my_model.created_at,
            'updated_at': my_model.updated_at,
            "name": "My First Model",
            "my_number": 89
        }
        my_old_updated_at = my_model.updated_at
        my_model.save()
        self.assertNotEqual(my_model.updated_at, my_old_updated_at)
