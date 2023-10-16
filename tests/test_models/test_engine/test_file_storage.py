#!/usr/bin/python3
"""  test for file_storage module"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
import models
import os
from models.engine.file_storage import FileStorage


class TestFilestorage(unittest.TestCase):
    """CLass created to test all the cases of FireStorage class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp.json")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp.json", "file.json")
        except IOError:
            pass

    def test_attr(self):
        """Tests FileStorage attributes"""
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_all(self):
        """testing the all method"""

        store = FileStorage()
        self.assertEqual(type(store.all()), dict)
        self.assertIs(store.all(), store._FileStorage__objects)

    def test_all_with_arg(self):
        """testing the all method with  arguments"""

        store1 = FileStorage()
        with self.assertRaises(TypeError):
            store1.all(25)

    def test_allnotempty(self):
        """test all after saving if it is emtpy or not"""
        base = BaseModel()
        base.save()
        dicts = models.storage.all()
        self.assertTrue(dicts)

    def test_new(self):
        """testing the new method"""

        base2 = BaseModel()
        base2.id = "897"
        store2 = FileStorage()
        store2.new(base2)
        self.assertIn("BaseModel.897", store2.all())

    def test_reload(self):
        """testing the reload method"""

        base3 = BaseModel()
        base3.id = "963"
        storage = FileStorage()
        storage.new(base3)
        base3.save()
        storage.reload()
        self.assertIn("BaseModel.963", storage.all())

    def test_reload_with_arg(self):
        """test reload with argument"""
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
