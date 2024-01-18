#!/usr/bin/python3
"""A unit test module for the console (command interpreter).
"""
import MySQLdb
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand, storage
from helpers.test_helpers import Helpers
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Represents the test class for the HBNBCommand class.
    """

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.cons = HBNBCommand()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests the create command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            self.cons.onecmd('create City name="Texas"')
            mdl_id = cout.getvalue().strip()
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            self.cons.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            self.cons.onecmd('create User name="James" age=17 height=5.9')
            mdl_id = cout.getvalue().strip()
            self.cons.onecmd('show User {}'.format(mdl_id))

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            # creating a model with non-null attribute(s)
            # creating a User instance
            helpers = Helpers()
            self.cons.onecmd(
                'create User email="john25@gmail.com" password="123"')
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            dbc.close()
            # with self.assertRaises(sqlalchemy.exc.OperationalError):
            #     cons.do_create("User")

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            # showing a User instance
            obj = User(email="john25@gmail.com", password="123")
            helpers = Helpers()
            # cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            # result = cursor.fetchone()
            # self.assertTrue(result is None)
            # self.cons.onecmd('show User {}'.format(obj.id))
            # self.assertEqual(
            #     cout.getvalue().strip(),
            #     '** no instance found **'
            # )
            # cursor = dbc.cursor()
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            storage.reload()
            self.cons.onecmd('show User {}'.format(obj.id))
            printed_result = cout.getvalue().splitlines()[0]
            self.assertIn('john25@gmail.com', printed_result)
            self.assertIn('123', printed_result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        helpers = Helpers()
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute('SELECT COUNT(*) FROM states;')
        res = cursor.fetchone()
        prev_count = int(res[0])
        self.cons.onecmd('create State name="Enugu"')
        helpers.stdout(lambda: self.cons.onecmd(
            'count State'), str(prev_count + 1)+"\n")
        cursor.close()
        dbc.close()
