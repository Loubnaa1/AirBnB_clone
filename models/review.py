#!/usr/bin/python3
"""contains the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """cantains the class  review."""

    place_id = ""
    user_id = ""
    text = ""
