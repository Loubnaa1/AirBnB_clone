#!/usr/bin/python3
"""Tests for the base_model module"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
import models
import os


class TestBaseModel(unittest.TestCase):
    """Class to test the BaseModel module"""

    def setUp(self):
        """Prepare test environment"""
        self.model = BaseModel()
        if os.path.exists("file.json"):
            os.rename("file.json", "temp.json")

    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists("file.json"):
            os.remove("file.json")
        if os.path.exists("temp.json"):
            os.rename("temp.json", "file.json")

    def test_attributes_existence_and_types(self):
        """Test attributes' existence and types"""
        self.model.name = "model"
        self.assertTrue(hasattr(self.model, "name"))
        self.assertEqual(str, type(self.model.id))
        self.assertEqual(str, type(self.model.name))
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)
        self.assertEqual(len(self.model.__dict__), 3)

    def test_string_representation(self):
        """Test string representation of object"""
        date = datetime.now()
        self.model.id = "116"
        self.model.created_at = self.model.updated_at = date
        expected_string = "[BaseModel] (116) {'id': '116', 'created_at': %r, 'updated_at': %r}" % (date, date)
        self.assertEqual(expected_string, str(self.model))

    def test_to_dict_method(self):
        """Test the to_dict method"""
        self.model.id = "117"
        self.assertEqual(self.model.id, self.model.to_dict()["id"])
        self.assertEqual(self.model.created_at.isoformat(), self.model.to_dict()["created_at"])
        self.assertEqual(self.model.updated_at.isoformat(), self.model.to_dict()["updated_at"])
        self.assertEqual("BaseModel", self.model.to_dict()["__class__"])

    def test_instance_creation(self):
        """Test instantiation of BaseModel"""
        self.assertIsInstance(self.model, BaseModel)

    def test_save_method_with_incorrect_args(self):
        """Test the save method with incorrect arguments"""
        with self.assertRaises(TypeError):
            self.model.save(None)

    def test_updated_at_after_save(self):
        """Test if updated_at attribute is modified after save"""
        old_updated = self.model.updated_at
        self.model.save()
        self.assertNotEqual(old_updated, self.model.updated_at)

    def test_instance_saved_to_file(self):
        """Test if the instance is saved to the JSON file after save"""
        self.model.save()
        with open("file.json", "r") as file:
            self.assertIn("BaseModel." + self.model.id, file.read())


if __name__ == "__main__":
    unittest.main()
