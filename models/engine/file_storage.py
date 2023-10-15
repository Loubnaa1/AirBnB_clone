#!/usr/bin/python3
"""Module encompassing the FileStorage class for managing JSON storage."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class to handle long-term storage of instances."""
    
    __file_path = "file.json"
    __objects = {}

    # A dict to facilitate dynamic instance creation, mapping class names to classes.
    CLASS_DICT = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def all(self):
        """Retrieve the complete dictionary of objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Insert a new object into the storage dictionary."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize the storage dictionary and save to a JSON file."""
        with open(FileStorage.__file_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in FileStorage.__objects.items()}, f)

    def reload(self):
        """Deserialize the JSON file to the storage dictionary, if it exists."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                objdict = json.load(f)
                for obj in objdict.values():
                    cls_name = obj.pop("__class__", None)  
                    if cls_name:
                        self.new(FileStorage.CLASS_DICT[cls_name](**obj))
        except FileNotFoundError:
            pass  
