#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py."""

import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    """Tests for checking instantiation of the FileStorage class."""

    def test_instance_creation_no_args(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_instance_creation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_path_private_attribute_type(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def test_objects_private_attribute_type(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initialization(self):
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Tests for various methods of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        if os.path.exists("file.json"):
            os.rename("file.json", "tmp")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("file.json"):
            os.remove("file.json")
        if os.path.exists("tmp"):
            os.rename("tmp", "file.json")
        FileStorage._FileStorage__objects = {}

    def test_all_method(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_method_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_method(self):
        objects = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for obj in objects:
            models.storage.new(obj)
            self.assertIn(f"{obj.__class__.__name__}.{obj.id}", models.storage.all().keys())
            self.assertIn(obj, models.storage.all().values())

    def test_new_method_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save_method(self):
        objects = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for obj in objects:
            models.storage.new(obj)

        models.storage.save()

        with open("file.json", "r") as file:
            content = file.read()
            for obj in objects:
                self.assertIn(f"{obj.__class__.__name__}.{obj.id}", content)

    def test_save_method_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_method(self):
        objects = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for obj in objects:
            models.storage.new(obj)

        models.storage.save()
        models.storage.reload()

        stored_objs = FileStorage._FileStorage__objects
        for obj in objects:
            self.assertIn(f"{obj.__class__.__name__}.{obj.id}", stored_objs)

    def test_reload_method_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
