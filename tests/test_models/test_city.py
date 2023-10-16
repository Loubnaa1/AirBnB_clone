#!/usr/bin/python3
"""
Unit tests for the city module.
"""
import unittest
from models.base_model import BaseModel
from models.city import City
from datetime import datetime
import os


class CityTests(unittest.TestCase):
    """Test cases for City class functionality."""

    def test_attributes_existence(self):
        """Check the presence of attributes in City instances."""

        city_instance = City()
        self.assertTrue(hasattr(city_instance, "name"))
        self.assertTrue(hasattr(city_instance, "id"))
        self.assertTrue(hasattr(city_instance, "created_at"))
        self.assertTrue(hasattr(city_instance, "updated_at"))
        self.assertTrue(hasattr(city_instance, "state_id"))
        self.assertIsInstance(city_instance.created_at, datetime)
        self.assertIsInstance(city_instance.updated_at, datetime)
        self.assertIsInstance(city_instance.id, str)
        self.assertIsInstance(city_instance.name, str)
        self.assertIsInstance(city_instance.state_id, str)

    def test_inheritance(self):
        """Verify the inheritance from BaseModel."""

        city_instance = City()
        self.assertIsInstance(city_instance, BaseModel)
        self.assertTrue(issubclass(City, BaseModel))

    def test_representation(self):
        """Check string representation of City instances."""

        city_instance = City()
        city_instance.id = "1111"
        current_date = datetime.now()
        city_instance.created_at = city_instance.updated_at = current_date
        date_str = repr(current_date)
        instance_str = str(city_instance)
        self.assertIn("[City] (1111)", instance_str)
        self.assertIn("'created_at': " + date_str, instance_str)
        self.assertIn("'updated_at': " + date_str, instance_str)
        self.assertIn("'id': '1111'", instance_str)

    def test_dictionary_conversion(self):
        """Test the to_dict method functionality."""

        city_instance = City()
        city_instance.id = "1113"
        creation_date = city_instance.created_at
        update_date = city_instance.updated_at
        class_name = type(city_instance).__name__
        self.assertEqual(city_instance.id, city_instance.to_dict()["id"])
        self.assertEqual(creation_date.isoformat(), city_instance.to_dict()["created_at"])
        self.assertEqual(update_date.isoformat(), city_instance.to_dict()["updated_at"])
        self.assertEqual(class_name, city_instance.to_dict()["__class__"])

    def test_save_method_exceptions(self):
        """Check the save method for exceptions with invalid arguments."""

        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.save(None)

    def test_updated_attribute_after_save(self):
        """Verify if updated_at attribute changes post save."""

        city_instance = City()
        previous_update = city_instance.updated_at
        city_instance.save()
        self.assertNotEqual(previous_update, city_instance.updated_at)

    def test_instance_persistence(self):
        """Confirm if saved instance is present in the JSON file."""

        city_instance = City()
        city_instance.save()
        instance_key = "City." + city_instance.id
        with open("file.json", "r") as file:
            self.assertIn(instance_key, file.read())

    @classmethod
    def setUpClass(cls):
        """Rename the JSON file if present."""

        try:
            os.rename("file.json", "temp.json")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Remove and restore the JSON file."""

        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp.json", "file.json")
        except IOError:
            pass


if __name__ == "__main__":
    unittest.main()
