#!/usr/bin/python3
""" Contains Review class """
from models.base_model import BaseModel


class Review(BaseModel):
    """creation of the class"""

    place_id = ""
    user_id = ""
    text = ""
