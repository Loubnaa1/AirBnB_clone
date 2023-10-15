#!/usr/bin/python3
""" Contains FileStorage Class """

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """Creation of the class"""

    __file_path = "file.json"
    __objects = {}

    def classes(self):
        """Returns a dictionary of valid classes and their references"""

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def all(self):
        """Method that return the dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """assign obj to __objects key
        the key is in this form <obj class name>.id"""

        key = str(obj.__class__.__name__) + "." + str(obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """converting python object to json string and save it to a json file
        'serialization'"""

        new_dict = {}
        keys_values = list(FileStorage.__objects.items())
        i = 0
        while i < len(keys_values):
            key, value = keys_values[i]
            new_dict[key] = value.to_dict()
            i += 1

        with open(FileStorage.__file_path, "w") as wf:
            json.dump(new_dict, wf)

    def reload(self):
        """From json file convert the json string to python object
        'deserialization'"""

        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as rf:
                pyth_obj = json.load(rf)

            dicts = {}
            keys_values = list(pyth_obj.items())
            i = 0
            while i < len(keys_values):
                key, val = keys_values[i]
                dicts[key] = FileStorage.all_classes[val["__class__"]](**val)
                i += 1

            FileStorage.__objects = dicts
