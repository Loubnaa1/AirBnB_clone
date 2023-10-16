#!/usr/bin/python3
"""contains the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """contains the class  User."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
