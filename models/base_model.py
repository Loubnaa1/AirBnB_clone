#!/usr/bin/python3
""" base_model is module containing the parent class 'BaseModel' """

import models
import uuid
from datetime import datetime


class BaseModel:
    """Creating The BaseModel Class"""

    def __init__(self, *args, **kwargs):
        """Constructor method"""

        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at":
                    self.created_at = datetime.fromisoformat(value)
                elif key == "updated_at":
                    self.updated_at = datetime.fromisoformat(value)
                elif key == "__class__":
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """converting the object to a human readable string"""

        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the public instance attribute updated_at with
        the current datetime"""

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all
        keys/values of __dict__ of the instance"""

        dicts = dict(self.__dict__)
        dicts["created_at"] = self.created_at.isoformat()
        dicts["updated_at"] = self.updated_at.isoformat()
        dicts["__class__"] = self.__class__.__name__
        return dicts
