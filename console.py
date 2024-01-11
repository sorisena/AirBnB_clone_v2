#!/usr/bin/python3
"""The Console Module"""
from models.base_model import BaseModel
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.place import Place
from models.state import State
import cmd
import re
from models import storage


class HBNBCommand(cmd.Cmd):
    """The class definition HBNBCommand"""

    prompt = '(hbnb) '
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
        }

    objs = storage.all()
    Dict_Check = 0

    def precmd(self, line):
        """parses input"""

        if '.' in line:
            if '{' in line or '}' in line:
                self.Dict_Check = quit
            else:
                self.Dict_Check = 0

            _delim = '.(", :){}'
            GetInput = re.split('[{}]+'.format(re.escape(_delim)), line)
            Res = GetInput[1]

            for i in range(len(GetInput) - 1):
                if i != 1:
                    Res += " " + GetInput[i].strip("'")

            return Res
        else:
            return line

    def emptyline(self):
        """Handle the empty line"""
        pass

    def do_quit(self, line):
        """Exit the program with Quit command"""
        return True

    def do_EOF(self, line):
        """Exit the program with EOF (ctrl+D) command"""
        return True

    def do_create(self, line):
        """Creates a new instance of a BaseModel class,
        saves it (to the JSON file) and prints the id.
        Ex: $ create BaseModel
        """

        if not line:
            print("** class name missing **")
        elif line not in self.classes.keys():
            print("** class doesn't exist **")
        else:
            NewInstance = self.classes[line]()
            NewInstance.save()
            print(NewInstance.id)

    def do_show(self, line):
        """Prints the string representation of an
        instance based on the class name and id.
        Ex: $ show BaseModel 1234-1234-1234.
        """

        if not line:
            print("** class name missing **")
        else:
            _Args = line.split()

            if _Args[0] not in self.classes.keys():
                print("** class doesn't exist **")
            elif len(_Args) < 2:
                print("** instance id missing **")
            else:
                key = f"{_Args[0]}.{_Args[1]}"
                if key in self.objs.keys():
                    print(self.objs[key])
                else:
                    print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and
        id (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234.
        """

        if not line:
            print("** class name missing **")
        else:
            _Args = line.split()

            if _Args[0] not in self.classes.keys():
                print("** class doesn't exist **")
            elif len(_Args) < 2:
                print("** instance id missing **")
            else:
                key = f"{_Args[0]}.{_Args[1]}"
                if key in self.objs.keys():
                    del self.objs[key]
                else:
                    print("** no instance found **")

    def do_all(self, line):
        """
        Prints all string representation of all instances
        based or not on the class name.
        Ex: $ all BaseModel or $ all.
        """

        Obj_List = []
        if not line:
            Obj_List = [obj.__str__() for obj in self.objs.values()]
            print(Obj_List)
        else:
            if line not in self.classes.keys():
                print("** class doesn't exist **")
            else:
                Obj_List = [
                        obj.__str__() for obj in self.objs.values()
                        if obj.__class__.__name__ == line
                        ]
                print(Obj_List)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com.
        """

        _ARGS = line.split()

        if len(_ARGS) >= 4:
            if _ARGS[0] not in self.classes.keys():
                print("** class doesn't exist **")
            else:
                key = f"{_ARGS[0]}.{_ARGS[1]}"

                if key in self.objs.keys():
                    if self.Dict_Check == 1:
                        for j in range(2, len(_ARGS), 2):
                            setattr(self.objs[key], _ARGS[j], _ARGS[j + 1])
                    else:
                        _ARGS[2] = _ARGS[2].strip('"')
                        _ARGS[3] = _ARGS[3].strip('"')
                        setattr(self.objs[key], _ARGS[2], _ARGS[3])
                    self.objs[key].save()
                else:
                    print("** no instance found **")
        elif len(_ARGS) == 3:
            print("** value missing **")
        elif len(_ARGS) == 2:
            print("** attribute name missing **")
        elif len(_ARGS) == 1:
            print("** instance id missing **")
        else:
            print("** class name missing **")

        self.Dict_Check = 0

    def do_count(self, line):
        """Retrieve the number of instances of a class."""
        count = 0

        for obj in self.objs.values():
            if obj.__class__.__name__ == line:
                count += 1

        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
