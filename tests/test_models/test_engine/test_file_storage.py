#!/usr/bin/python3
"""Unit tests for models/engine/file_storage.py."""

import os
import json
import models
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    """Tests for checking the instantiation of FileStorage class."""

    def test_instance_creation(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_instance_creation_with_argument(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_path_type(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def test_objects_type(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_type(self):
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Tests for different methods in the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        cls.models_instance_names = ["BaseModel", "User", "State", "City", "Place", "Amenity", "Review"]
        cls.models_instances = [BaseModel(), User(), State(), City(), Place(), Amenity(), Review()]

    @classmethod
    def setUp(cls):
        cls.storage = FileStorage()
        cls.storage_path = "file.json"
        if os.path.exists(cls.storage_path):
            os.rename(cls.storage_path, "temp.json")

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.storage_path):
            os.remove(cls.storage_path)
        if os.path.exists("temp.json"):
            os.rename("temp.json", cls.storage_path)
        FileStorage._FileStorage__objects = {}

    def test_all_method(self):
        self.assertIsInstance(self.storage.all(), dict)

    def test_all_method_with_argument(self):
        with self.assertRaises(TypeError):
            self.storage.all(None)

    def create_and_verify(self, instance, instance_name):
        """Helper function: Create and verify if object is stored properly."""
        self.storage.new(instance)
        key = f"{instance_name}.{instance.id}"
        self.assertIn(key, self.storage.all().keys())
        self.assertIn(instance, self.storage.all().values())

    def test_new_method(self):
        for instance_name, instance in zip(self.models_instance_names, self.models_instances):
            self.create_and_verify(instance, instance_name)

    def test_new_method_with_additional_arguments(self):
        with self.assertRaises(TypeError):
            self.storage.new(BaseModel(), 1)

    def save_and_verify(self, instance, instance_name):
        """Helper function: Save and verify if object is stored in file properly."""
        self.storage.save()
        with open(self.storage_path, "r") as f:
            saved_text = f.read()
            self.assertIn(instance_name + "." + instance.id, saved_text)

    def test_save_method(self):
        for instance_name, instance in zip(self.models_instance_names, self.models_instances):
            self.storage.new(instance)
            self.save_and_verify(instance, instance_name)

    def test_save_method_with_argument(self):
        with self.assertRaises(TypeError):
            self.storage.save(None)

    def reload_and_verify(self, instance, instance_name):
        """Helper function: Reload and verify if object is loaded properly."""
        self.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn(instance_name + "." + instance.id, objs)

    def test_reload_method(self):
        for instance_name, instance in zip(self.models_instance_names, self.models_instances):
            self.storage.new(instance)
            self.storage.save()
            self.reload_and_verify(instance, instance_name)

    def test_reload_method_with_argument(self):
        with self.assertRaises(TypeError):
            self.storage.reload(None)

            
if __name__ == "__main__":
    unittest.main()
