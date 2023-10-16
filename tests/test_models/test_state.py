#!/usr/bin/python3
"""Unit tests for State module."""
import models
import unittest
from models.base_model import BaseModel
from models.state import State
from datetime import datetime
import os


class StateTestCase(unittest.TestCase):
    """Tests for State class."""

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
        state = State()
        attrs = ["name", "id", "created_at", "updated_at"]
        for attr in attrs:
            self.assertTrue(hasattr(state, attr), f"{attr} not found in State")

    def test_attributes_type(self):
        """Ensure all attributes have the correct type."""
        state = State()
        self.assertIsInstance(state.id, str)
        self.assertIsInstance(state.created_at, datetime)
        self.assertIsInstance(state.updated_at, datetime)
        self.assertIsInstance(state.name, str)

    def test_inheritance_from_base_model(self):
        """Ensure State is a subclass of BaseModel."""
        self.assertTrue(issubclass(State, BaseModel))

    def test_str_representation(self):
        """Test the string representation of the State object."""
        state = State()
        state.id = "SXYZ12345"
        date = datetime.now()
        state.created_at = state.updated_at = date
        date_repr = repr(date)
        string = str(state)
        self.assertIn("[State] (SXYZ12345)", string)
        self.assertIn("'created_at': " + date_repr, string)
        self.assertIn("'updated_at': " + date_repr, string)
        self.assertIn("'id': 'SXYZ12345'", string)

    def test_to_dict_method(self):
        """Test the to_dict method of the State class."""
        state = State()
        state.id = "SABC98765"
        self.assertEqual(state.id, state.to_dict()["id"])
        self.assertEqual(state.created_at.isoformat(), state.to_dict()["created_at"])
        self.assertEqual(state.updated_at.isoformat(), state.to_dict()["updated_at"])
        self.assertEqual("State", state.to_dict()["__class__"])

    def test_save_method(self):
        """Test the save method of the State class."""
        state = State()
        old_updated = state.updated_at
        state.save()
        self.assertNotEqual(old_updated, state.updated_at)

        # Ensure instance is saved in the json file
        representation = "State." + state.id
        with open("file.json", "r") as file:
            self.assertIn(representation, file.read())

        # Ensure save method does not accept any arguments apart from self
        with self.assertRaises(TypeError):
            state.save(None)

if __name__ == "__main__":
    unittest.main()
