#!/usr/bin/python3
"""Unit tests for User module."""
import unittest
from models.user import User
from datetime import datetime


class UserTestCase(unittest.TestCase):
    """Test cases for User class."""

    def setUp(self):
        """Set up method for testing."""
        self.user = User()

    def test_attribute_existence(self):
        """Ensure all required attributes are present."""
        attrs = ["id", "created_at", "updated_at", "email", "password", "first_name", "last_name"]
        for attr in attrs:
            with self.subTest(attr=attr):
                self.assertTrue(hasattr(self.user, attr), f"'{attr}' attribute missing in User class.")

    def test_attribute_type(self):
        """Ensure all attributes have the correct type."""
        attr_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "email": str,
            "password": str,
            "first_name": str,
            "last_name": str
        }
        for attr, expected_type in attr_types.items():
            with self.subTest(attr=attr, expected_type=expected_type):
                self.assertIsInstance(getattr(self.user, attr), expected_type, f"'{attr}' has incorrect type in User class.")


if __name__ == "__main__":
    unittest.main()
