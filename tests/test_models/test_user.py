#!/usr/bin/python3
""" """

import unittest
from models.user import User


class test_User(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.user = User(
            first_name="David",
            last_name="David",
            email="David@eam.com",
            password="P@sswssf",
        )

    def test_first_name(self):
        """ """
        new = self.user
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.user
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        new = self.user
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        new = self.user
        self.assertEqual(type(new.password), str)
