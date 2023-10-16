#!/usr/bin/python3
"""
Defines the FileStorage class responsible for serialization and deserialization
of instances to and from a JSON file.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """A class to manage the serialization and deserialization of instances.

    Attributes:
        __file_path (str): Path to the file for storing serialized objects.
        __objects (dict): Dictionary storing all objects by <class-name>.id
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Retrieve the dictionary of all stored objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to the storage dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize the storage dictionary to a JSON file."""
        serialized_data = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(serialized_data, f)

    def reload(self):
        """Deserialize data from the JSON file to the storage dictionary."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                loaded_data = json.load(f)
                for instance_data in loaded_data.values():
                    class_name = instance_data.pop("__class__")
                    self.new(eval(class_name)(**instance_data))
        except FileNotFoundError:
            pass
