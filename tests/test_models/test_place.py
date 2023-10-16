#!/usr/bin/python3
"""Unit tests for Place module."""
import unittest
from models.base_model import BaseModel
from models.place import Place
from datetime import datetime
import os


class PlaceTestCase(unittest.TestCase):
    """Tests for Place class."""

    @classmethod
    def setUpClass(cls):
        """Rename existing 'file.json' if it exists before any test runs."""
        try:
            os.rename("file.json", "temp.json")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests: Remove 'file.json' and restore the original if it existed."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp.json", "file.json")
        except IOError:
            pass

    def test_attributes_existence(self):
        """Ensure all required attributes are present."""
        place = Place()
        attrs = ["longitude", "user_id", "amenity_ids", "city_id", "name", "description",
                 "number_rooms", "number_bathrooms", "max_guest", "price_by_night", "latitude",
                 "created_at", "updated_at"]
        for attr in attrs:
            self.assertTrue(hasattr(place, attr), f"{attr} not found in Place")

    def test_attributes_type(self):
        """Ensure all attributes have the correct type."""
        place = Place()
        self.assertIsInstance(place.number_rooms, int)
        self.assertIsInstance(place.longitude, float)
        self.assertIsInstance(place.latitude, float)
        self.assertIsInstance(place.amenity_ids, list)
        self.assertIsInstance(place.city_id, str)
        self.assertIsInstance(place.user_id, str)
        self.assertIsInstance(place.max_guest, int)
        self.assertIsInstance(place.price_by_night, int)
        self.assertIsInstance(place.description, str)
        self.assertIsInstance(place.name, str)
        self.assertIsInstance(place.number_bathrooms, int)
        self.assertIsInstance(place.created_at, datetime)
        self.assertIsInstance(place.updated_at, datetime)

    def test_inheritance_from_base_model(self):
        """Ensure Place is a subclass of BaseModel."""
        self.assertTrue(issubclass(Place, BaseModel))

    def test_str_representation(self):
        """Test the string representation of the Place object."""
        place = Place()
        place.id = "XYZ12345"
        date = datetime.now()
        place.created_at = place.updated_at = date
        date_repr = repr(date)
        string = str(place)
        self.assertIn("[Place] (XYZ12345)", string)
        self.assertIn("'created_at': " + date_repr, string)
        self.assertIn("'updated_at': " + date_repr, string)
        self.assertIn("'id': 'XYZ12345'", string)

    def test_to_dict_method(self):
        """Test the to_dict method of the Place class."""
        place = Place()
        place.id = "ABC98765"
        self.assertEqual(place.id, place.to_dict()["id"])
        self.assertEqual(place.created_at.isoformat(), place.to_dict()["created_at"])
        self.assertEqual(place.updated_at.isoformat(), place.to_dict()["updated_at"])
        self.assertEqual("Place", place.to_dict()["__class__"])

    def test_save_method(self):
        """Test the save method of the Place class."""
        place = Place()
        old_updated = place.updated_at
        place.save()
        self.assertNotEqual(old_updated, place.updated_at)

        representation = "Place." + place.id
        with open("file.json", "r") as file:
            self.assertIn(representation, file.read())

        with self.assertRaises(TypeError):
            place.save(None)

if __name__ == "__main__":
    unittest.main()
