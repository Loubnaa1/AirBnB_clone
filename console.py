#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from models import storage
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def extract_tokens(argument):
    """Parses the argument into a list of tokens."""
    curly_content = re.search(r"\{(.*?)\}", argument)
    bracket_content = re.search(r"\[(.*?)\]", argument)
    tokens = []
    
    if curly_content:
        tokens.extend(split(argument[:curly_content.span()[0]]))
        tokens.append(curly_content.group())
    elif bracket_content:
        tokens.extend(split(argument[:bracket_content.span()[0]]))
        tokens.append(bracket_content.group())
    else:
        tokens.extend(split(argument))

    return [token.strip(",") for token in tokens]


class HBNBCommand(cmd.Cmd):
    """HolbertonBnB command interpreter."""
    prompt = "(hbnb) "
    SUPPORTED_CLASSES = {
        "BaseModel", "User", "State", "City", "Place", "Amenity", "Review"
    }

    def emptyline(self):
        pass

    def _parse_input(self, arg):
        """Parses the default input to get class and command."""
        match_class = re.search(r"\.", arg)
        if not match_class:
            return None, None
        class_name, command_str = arg.split(".", 1)
        match_cmd = re.search(r"\((.*?)\)", command_str)
        if not match_cmd:
            return None, None
        cmd_name, cmd_args = command_str.split("(", 1)
        cmd_args = cmd_args.rstrip(")")
        return class_name, (cmd_name, cmd_args)

    def default(self, arg):
        class_name, command = self._parse_input(arg)
        if not class_name or not command:
            print("*** Unknown syntax:", arg)
            return

        cmd_name, cmd_args = command
        method_name = "do_" + cmd_name
        if hasattr(self, method_name):
            getattr(self, method_name)(f"{class_name} {cmd_args}")
        else:
            print("*** Unknown syntax:", arg)

    def do_quit(self, _):
        return True

    def do_EOF(self, _):
        print()
        return True

    def _get_obj(self, class_name, obj_id):
        """Retrieve object by class name and id."""
        return storage.all().get(f"{class_name}.{obj_id}")

    def _class_exists(self, class_name):
        return class_name in self.SUPPORTED_CLASSES

    def do_create(self, arg):
        args = extract_tokens(arg)
        if not args:
            print("** class name missing **")
            return
        if not self._class_exists(args[0]):
            print("** class doesn't exist **")
            return
        instance = eval(args[0])()
        print(instance.id)
        storage.save()

    def do_show(self, arg):
        args = extract_tokens(arg)
        if not args:
            print("** class name missing **")
            return
        if not self._class_exists(args[0]):
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj = self._get_obj(args[0], args[1])
        if not obj:
            print("** no instance found **")
            return
        print(obj)

    def do_destroy(self, arg):
        args = extract_tokens(arg)
        if not args:
            print("** class name missing **")
            return
        if not self._class_exists(args[0]):
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_key = f"{args[0]}.{args[1]}"
        if obj_key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[obj_key]
        storage.save()

    def do_all(self, arg):
        args = extract_tokens(arg)
        if args and not self._class_exists(args[0]):
            print("** class doesn't exist **")
            return
        obj_list = []
        for obj in storage.all().values():
            if not args or (args and obj.__class__.__name__ == args[0]):
                obj_list.append(obj.__str__())
        print(obj_list)

    def do_update(self, arg):
        args = extract_tokens(arg)
        if not args:
            print("** class name missing **")
            return
        if not self._class_exists(args[0]):
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj = self._get_obj(args[0], args[1])
        if not obj:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(obj, args[2], args[3])
        storage.save()

if __name__ == "__main__":
    HBNBCommand().cmdloop()
