#!/usr/bin/python3
"""contains the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""
        if kwargs:
            self.id = kwargs.get('id', str(uuid4()))
            self.created_at = datetime.strptime(kwargs.get('created_at', datetime.today().isoformat()), self.DATE_FORMAT)
            self.updated_at = datetime.strptime(kwargs.get('updated_at', datetime.today().isoformat()), self.DATE_FORMAT)
            
            # Exclude these from kwargs
            kwargs.pop('id', None)
            kwargs.pop('created_at', None)
            kwargs.pop('updated_at', None)

            # Update other attributes
            self.__dict__.update(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            models.storage.new(self)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance."""
        rdict = {**self.__dict__, 
                 "created_at": self.created_at.isoformat(),
                 "updated_at": self.updated_at.isoformat(),
                 "__class__": self.__class__.__name__}
        return rdict

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
