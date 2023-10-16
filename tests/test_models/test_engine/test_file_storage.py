#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review

class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def testFileStorage_objects_is_private_dict(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initializes(self):
        self.assertIsInstance(models.storage, FileStorage)

class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        cls.bm = BaseModel()
        cls.us = User()
        cls.st = State()
        cls.pl = Place()
        cls.cy = City()
        cls.am = Amenity()
        cls.rv = Review()
        cls.objs = [cls.bm, cls.us, cls.st, cls.pl, cls.cy, cls.am, cls.rv]
        cls.model_names = [
            "BaseModel", "User", "State", 
            "Place", "City", "Amenity", "Review"
        ]

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
    
    def setUp(self):
        self.storage = FileStorage()
        for obj in self.objs:
            models.storage.new(obj)

    def tearDown(self):
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        for obj, name in zip(self.objs, self.model_names):
            with self.subTest(obj=obj, name=name):
                self.assertIn(f"{name}.{obj.id}", models.storage.all().keys())
                self.assertIn(obj, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        models.storage.save()
        with open("file.json", "r") as f:
            save_text = f.read()
            for obj, name in zip(self.objs, self.model_names):
                with self.subTest(obj=obj, name=name):
                    self.assertIn(f"{name}.{obj.id}", save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        for obj, name in zip(self.objs, self.model_names):
            with self.subTest(obj=obj, name=name):
                self.assertIn(f"{name}.{obj.id}", objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

if __name__ == "__main__":
    unittest.main()
