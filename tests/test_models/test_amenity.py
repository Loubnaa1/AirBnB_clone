#!/usr/bin/python3
"""Defines unittests for models/amenity.py."""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class BaseTestAmenity(unittest.TestCase):
    """Base Test class for setting up Amenity tests."""
    @classmethod
    def setUpClass(cls):
        cls.amenity = Amenity()

    @classmethod
    def tearDownClass(cls):
        del cls.amenity
        try:
            os.remove("file.json")
        except:
            pass


class TestAmenityInstantiation(BaseTestAmenity):
    """Tests for Amenity instantiation."""

    def test_instance(self):
        self.assertIsInstance(self.amenity, Amenity)

    def test_id(self):
        self.assertIsInstance(self.amenity.id, str)

    def test_created_at(self):
        self.assertIsInstance(self.amenity.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.amenity.updated_at, datetime)

    def test_name_attribute(self):
        self.assertTrue(hasattr(Amenity, 'name'))
        self.assertFalse(hasattr(self.amenity, 'name'))

    def test_unique_ids(self):
        am2 = Amenity()
        self.assertNotEqual(self.amenity.id, am2.id)

    def test_unique_times(self):
        am2 = Amenity()
        self.assertNotEqual(self.amenity.created_at, am2.created_at)
        self.assertNotEqual(self.amenity.updated_at, am2.updated_at)

    def test_str_representation(self):
        a_str = str(self.amenity)
        self.assertIn("[Amenity] ({})".format(self.amenity.id), a_str)

    def test_kwargs_instantiation(self):
        am_dict = self.amenity.to_dict()
        am2 = Amenity(**am_dict)
        self.assertEqual(am2.to_dict(), am_dict)


class TestAmenitySave(BaseTestAmenity):
    """Tests for the Amenity save method."""

    def test_save(self):
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertNotEqual(self.amenity.updated_at, old_updated_at)

    def test_save_to_file(self):
        self.amenity.save()
        with open("file.json", "r") as f:
            self.assertIn("Amenity.{}".format(self.amenity.id), f.read())


class TestAmenityToDict(BaseTestAmenity):
    """Tests for the Amenity to_dict method."""

    def test_to_dict(self):
        a_dict = self.amenity.to_dict()
        self.assertIsInstance(a_dict, dict)
        self.assertIn("__class__", a_dict)
        self.assertEqual(a_dict["__class__"], "Amenity")
        self.assertIn("id", a_dict)
        self.assertIn("created_at", a_dict)
        self.assertIn("updated_at", a_dict)


if __name__ == "__main__":
    unittest.main()
