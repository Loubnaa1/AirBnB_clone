#!/usr/bin/python3
"""Definition of the FileStorage class."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """A class representing a storage engine.

    Attributes:
        __file_path (str): The path to the file for saving objects.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Retrieve the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add obj to __objects with key '<obj_class_name>.id'."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (__file_path)."""
        serializable_dict = {
            key: obj.to_dict() for key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as file:
            json.dump(serializable_dict, file)

    def reload(self):
        """Deserialize the JSON file (__file_path) to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path, "r") as file:
                deserialized_objects = json.load(file)
                for obj_data in deserialized_objects.values():
                    class_name = obj_data.pop("__class__")
                    self.new(eval(class_name)(**obj_data))
        except FileNotFoundError:
            pass
