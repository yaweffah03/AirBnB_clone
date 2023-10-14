#!/usr/bin/python3
"""The command prompt class - HBNBCommand"""


import cmd
from models import storage
import models
import re
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def split_arg(arg):
    """splits the arguments into a string array"""
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


def convert(val):
    """converts value to proper type"""
    constructors = [int, float, str]
    for c in constructors:
        try:
            return c(val)
        except ValueError:
            pass


def find_models(args):
    data = storage.all()
    data_list = []
    arg_list = split_arg(args)
    classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    if len(args) == 0:
        for value in data.values():
            data_list.append(str(value))
    elif arg_list[0] not in classes:
        print("** class doesn't exist **")
        return
    else:
        for value in data.values():
            if value.__class__.__name__ == arg_list[0]:
                data_list.append(str(value))
    return data_list


class HBNBCommand(cmd.Cmd):
    """The Command prompt Class"""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    # def __init__(self):
    #     """Initialization"""
    #     cmd.Cmd.__init__(self)

    def do_EOF(self, arg):
        """Quit console"""
        print("")
        return True

    def emptyline(self):
        """empty line. Do nothing"""
        pass

    def do_quit(self, arg):
        """Quits the program."""
        return True

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, args):
        """  Usage: create <className>
        creates a new instance of BaseModel and saves it to a file
        and prints the id
        """
        arg_list = split_arg(args)

        if len(args) == 0:
            print("** class name missing **")
            return False
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        else:
            # new_model = classes[arg_list[0]]()
            new_model = eval(arg_list[0])()
            print(new_model.id)
            storage.save()

    def do_show(self, args):
        """Usage: show <className> <id> or <className>.show<id>
        Prints the string representation of an
        instance based on the class name and id
        """
        arg_list = split_arg(args)

        if len(args) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        else:
            data = storage.all()
            key = "{}.{}".format(arg_list[0], arg_list[1])
            if key in data:
                print(data[key])
            else:
                print("** no instance found **")

    def do_destroy(self, args):
        """ Usage: destroy <className> <id>
        Deletes an instance based on the class name and id
        """
        arg_list = split_arg(args)

        if len(args) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(arg_list[0], arg_list[1])
            data = storage.all()
            if key in data:
                storage.delete(key)
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, args):
        """Usage: all or all <className> or <className>.all()
        Prints all string representation
        of all instances based or not on the class name
        """
        data_list = find_models(args)
        if data_list is not None:
            print(data_list)

    def do_update(self, args):
        """Usage: update <className> <id> <attribute> <value>
        Updates an instance based on the class name
        and id by adding or updating attribute
        """
        arg_list = split_arg(args)

        if len(args) == 0:
            print("** class name missing **")
            return False
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        elif len(arg_list) <= 1:
            print("** instance id missing **")
            return False
        else:
            key = "{}.{}".format(arg_list[0], arg_list[1])
            data = storage.all()
            if key in data:
                if len(arg_list) == 2:
                    print("** attribute name missing **")
                    return False
                elif len(arg_list) == 3:
                    print("** value missing **")
                    return False
                else:
                    storage.update(key, arg_list[2], convert(arg_list[3]))
                    model = data[key]
                    model.save()
            else:
                print("** no instance found **")
                return False

    # def onecmd(self, s):
    #     return cmd.Cmd.onecmd(self, s)

    # def precmd(self, line):
    #     p = r"^(\w*)\.(\w+)(?:\(([^)]*)\))$"
    #     m = re.search(p, line)
    #     if not m:
    #         return line
    #     command = m.group(2) + " " + m.group(1) + " " + m.group(3)
    #     # self.onecmd(command)
    #     return command
    #     # return cmd.Cmd.precmd(self, line)

    def do_count(self, args):
        """Usage: count <className> or <className>.count()
        retrieves the number of instances of a class
        """
        data_list = find_models(args)
        if data_list is not None:
            print(len(data_list))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
