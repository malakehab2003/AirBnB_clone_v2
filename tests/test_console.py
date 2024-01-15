#!/usr/bin/python3
"""
Update the def do_create(self, arg): function of your command interpreter (console.py) to allow for object creation with given parameters:

Command syntax: create <Class name> <param 1> <param 2> <param 3>...
Param syntax: <key name>=<value>
Value syntax:
String: "<value>" => starts with a double quote
any double quote inside the value must be escaped with a backslash \
all underscores _ must be replace by spaces . Example: You want to set the string My little house to the attribute name, your command line must be name="My_little_house"
Float: <unit>.<decimal> => contains a dot .
Integer: <number> => default case
If any parameter doesn’t fit with these requirements or can’t be recognized correctly by your program, it must be skipped
"""
from console import HBNBCommand, BaseModel, \
    City, Amenity, Place, Review, State, User, storage
from helpers.test_helpers import Helpers
import unittest
import datetime
from uuid import UUID
import json
import os


class test_new_console_feature(unittest.TestCase):
    """
    test Feature
    """

    def setUp(self):
        """
        clear file.json
        """
        try:
            os.remove('file.json')
            storage.clear()
        except:
            pass

    def tearDown(self):
        """
        clear file.json
        """
        try:
            os.remove('file.json')
            storage.clear()
        except:
            pass

    def test_creation(self):
        """
        test feature
        """
        cmd = HBNBCommand()
        helpers = Helpers()
        cmd.do_create('State name="California"')
        self.assertEqual(len(storage.all()), 1)
        cmd.do_create('State name="California_Store"')
        self.assertEqual(len(storage.all()), 2)
        self.assertEqual(list(storage.all().values())
                         [1].name, "California Store")

    def test_wrong_creation(self):
        """
        test wrong param
        """
        cmd = HBNBCommand()
        helpers = Helpers()
        cmd.do_create('State name=5.5.3')
        cmd.do_all("State")
        self.assertEqual(len(storage.all()), 1)
        self.assertEqual(list(storage.all().values())[0].name, "")
        helpers.stdout(lambda: cmd.do_create(
            'Stated name=5.5.3'), "** class doesn't exist **\n")
