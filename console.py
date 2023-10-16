#!/usr/bin/python3
import cmd
from models import storage
from models.base_model import BaseModel
from shlex import split


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    __classes = {"BaseModel"}  # This can be extended with other classes

    def do_create(self, arg):
        """Create an instance of a class"""
        if not arg:
            print("** class name missing **")
            return
        if arg in HBNBCommand.__classes:
            new_instance = eval(arg)()
            print(new_instance.id)
            new_instance.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Show an instance based on class name and id"""
        args = split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Delete an instance based on class name and id"""
        args = split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Display all instances of a class"""
        if not arg:
            print([str(v) for v in storage.all().values()])
        elif arg in HBNBCommand.__classes:
            print([str(v) for k, v in storage.all().items() if arg in k])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Update an instance based on the class name and id"""
        args = split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        if args[2] not in ['id', 'created_at', 'updated_at']:
            setattr(storage.all()[key], args[2], type(getattr(storage.all()[key], args[2], ""))(args[3]))
            storage.save()

    def do_EOF(self, arg):
        """Exit the command interpreter"""
        print()
        return True

    def do_quit(self, arg):
        """Quit the command interpreter"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
