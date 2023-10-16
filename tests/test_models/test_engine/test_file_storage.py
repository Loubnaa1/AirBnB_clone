#!/usr/bin/python3
"""
Unit tests for file_storage.py within models/engine.
Test Classes:
    FileStorageCreationTests
    FileStorageFunctionalityTests
"""

import unittest
import os
import json
import models
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorageCreationTests(unittest.TestCase):
    """Tests for the instantiation of FileStorage."""

    def test_default_creation(self):
        storage_instance = FileStorage()
        self.assertIsInstance(storage_instance, FileStorage)

    def test_unexpected_args(self):
        with self.assertRaises(TypeError):
            FileStorage("Unexpected")

    def test_file_path_type(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def test_objects_type(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initialization(self):
        self.assertIsInstance(models.storage, FileStorage)


class FileStorageFunctionalityTests(unittest.TestCase):
    """Tests for the functionality of FileStorage."""

    @classmethod
    def setUpClass(cls):
        if os.path.isfile("file.json"):
            os.rename("file.json", "backup_file.json")

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile("file.json"):
            os.remove("file.json")
        if os.path.isfile("backup_file.json"):
            os.rename("backup_file.json", "file.json")
        FileStorage._FileStorage__objects.clear()

    def test_all_returns_dict(self):
        storage_data = models.storage.all()
        self.assertIsInstance(storage_data, dict)

    def test_all_unexpected_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all("Unexpected")

    def test_new_and_all(self):
        sample_instance = BaseModel()
        models.storage.new(sample_instance)
        storage_data = models.storage.all()
        key = "BaseModel." + sample_instance.id
        self.assertIn(key, storage_data)

    def test_new_extra_args(self):
        sample = BaseModel()
        with self.assertRaises(TypeError):
            models.storage.new(sample, "extra")

    def test_save_and_reload(self):
        instance_1 = BaseModel()
        key_1 = "BaseModel." + instance_1.id
        models.storage.new(instance_1)
        models.storage.save()

        FileStorage._FileStorage__objects.clear()

        self.assertNotIn(key_1, FileStorage._FileStorage__objects)
        models.storage.reload()
        self.assertIn(key_1, FileStorage._FileStorage__objects)

    def test_reload_unexpected_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload("Unexpected")


if __name__ == "__main__":
    unittest.main()
