#!/usr/bin/python3
"""Defines the HBnB console."""

import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    for pattern in [r"\{(.*?)\}", r"\[(.*?)\]"]:
        match = re.search(pattern, arg)
        if match:
            prefix = re.split(pattern, arg)[0]
            return [i.strip(",") for i in prefix.split()] + [match.group()]
    return [i.strip(",") for i in arg.split()]


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""
    
    prompt = "(hbnb) "
    CLASSES = {"BaseModel", "User", "State", "City", "Place", "Amenity", "Review"}

    def do_quit(self, _):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, _):
        """EOF signal to exit the program."""
        print("")
        return True

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Handle unregistered commands and methods."""
        try:
            method, args = re.split(r'\.| ', arg)
            if method in self.CLASSES and hasattr(self, f"do_{args.split('(')[0]}"):
                getattr(self, f"do_{args.split('(')[0]}")(f"{method} {args.split('(')[1][:-1]}")
            else:
                raise ValueError
        except ValueError:
            print(f"*** Unknown syntax: {arg}")

    def do_create(self, arg):
        """Create a new instance."""
        self._generic_error_handler(arg, "create")

    def do_show(self, arg):
        """Show an instance based on its ID."""
        self._generic_error_handler(arg, "show")

    def do_destroy(self, arg):
        """Destroy an instance based on its ID."""
        self._generic_error_handler(arg, "destroy")

    def do_all(self, arg):
        """Show all instances or instances of a specific class."""
        self._generic_error_handler(arg, "all")

    def do_count(self, arg):
        """Count instances of a specific class."""
        self._generic_error_handler(arg, "count")

    def do_update(self, arg):
        """Update an instance."""
        self._generic_error_handler(arg, "update")

    def _generic_error_handler(self, arg, operation):
        """Generic error handling and delegation to actual functions."""
        args = parse(arg)
        
        if not args:
            self._print_error_msg("class name missing")
            return
        
        if args[0] not in self.CLASSES:
            self._print_error_msg("class doesn't exist")
            return

        if operation in ["show", "destroy", "update"] and len(args) < 2:
            self._print_error_msg("instance id missing")
            return
        
        # Delegate to corresponding functions
        func_mapping = {
            "create": self._do_actual_create,
            "show": self._do_actual_show,
            "destroy": self._do_actual_destroy,
            "all": self._do_actual_all,
            "count": self._do_actual_count,
            "update": self._do_actual_update,
        }

        func_mapping[operation](args)

    # ... [Actual implementations for create, show, destroy, etc. functions similar to the original]

    @staticmethod
    def _print_error_msg(error_key):
        """Utility to print error messages."""
        error_messages = {
            "class name missing": "** class name missing **",
            "class doesn't exist": "** class doesn't exist **",
            "instance id missing": "** instance id missing **",
            "no instance found": "** no instance found **",
        }
        print(error_messages.get(error_key, "*** Unknown error ***"))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
