#!/usr/bin/python3
""" Contains User class """
from models.base_model import BaseModel


class User(BaseModel):
    """Creation of the User Class"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
