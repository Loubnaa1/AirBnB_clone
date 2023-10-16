#!/usr/bin/python3
"""Unit tests for Review module."""
import unittest
from models.base_model import BaseModel
from models.review import Review
from datetime import datetime
import os


class ReviewTestCase(unittest.TestCase):
    """Tests for Review class."""

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
        review = Review()
        attrs = ["user_id", "place_id", "text", "id", "created_at", "updated_at"]
        for attr in attrs:
            self.assertTrue(hasattr(review, attr), f"{attr} not found in Review")

    def test_attributes_type(self):
        """Ensure all attributes have the correct type."""
        review = Review()
        self.assertIsInstance(review.user_id, str)
        self.assertIsInstance(review.place_id, str)
        self.assertIsInstance(review.text, str)
        self.assertIsInstance(review.id, str)
        self.assertIsInstance(review.created_at, datetime)
        self.assertIsInstance(review.updated_at, datetime)

    def test_inheritance_from_base_model(self):
        """Ensure Review is a subclass of BaseModel."""
        self.assertTrue(issubclass(Review, BaseModel))

    def test_str_representation(self):
        """Test the string representation of the Review object."""
        review = Review()
        review.id = "RXYZ12345"
        date = datetime.now()
        review.created_at = review.updated_at = date
        date_repr = repr(date)
        string = str(review)
        self.assertIn("[Review] (RXYZ12345)", string)
        self.assertIn("'created_at': " + date_repr, string)
        self.assertIn("'updated_at': " + date_repr, string)
        self.assertIn("'id': 'RXYZ12345'", string)

    def test_to_dict_method(self):
        """Test the to_dict method of the Review class."""
        review = Review()
        review.id = "RABC98765"
        self.assertEqual(review.id, review.to_dict()["id"])
        self.assertEqual(review.created_at.isoformat(), review.to_dict()["created_at"])
        self.assertEqual(review.updated_at.isoformat(), review.to_dict()["updated_at"])
        self.assertEqual("Review", review.to_dict()["__class__"])

    def test_save_method(self):
        """Test the save method of the Review class."""
        review = Review()
        old_updated = review.updated_at
        review.save()
        self.assertNotEqual(old_updated, review.updated_at)

        representation = "Review." + review.id
        with open("file.json", "r") as file:
            self.assertIn(representation, file.read())

        with self.assertRaises(TypeError):
            review.save(None)

if __name__ == "__main__":
    unittest.main()
