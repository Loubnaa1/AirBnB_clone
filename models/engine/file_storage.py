#!/usr/bin/python3
""" module containing FileStorage Class """

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
    """Creating the class"""

    __file_path = "file.json"
    __objects = {}

    all_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

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
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict()

        with open(FileStorage.__file_path, "w") as wf:
            json.dump(new_dict, wf)

    def reload(self):
        """From json file convert the json string to python object
        'deserialization'"""

        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as rf:
                pyth_obj = json.load(rf)

            dicts = {}
            for key, val in pyth_obj.items():
                # s = key.split(".")[0]
                # dicts[key] = FileStorage.all_classes[s](**val)

                dicts[key] = FileStorage.all_classes[val["__class__"]](**val)

            FileStorage.__objects = dicts
        else:
            return
