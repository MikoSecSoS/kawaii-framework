# -*- coding:utf-8 -*-

import os
import re
import sys
import inspect

import logging

from lib.config import __version__
from lib.core.base import BaseInterpreter

from importlib import import_module

from rich.table import Table
from rich.console import Console
from termcolor import colored

logging.basicConfig(level=logging.INFO,
            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class Parser(BaseInterpreter):
    """docstring for Parser"""
    def __init__(self):
        super(Parser, self).__init__()
        
    #-------------------------------Command-------------------------------

    def help(self):
        """Show help
        """
        info = """
Core Commands
=============

    Command       Description
    -------       -----------
    ?             Help menu
    cd            Change the current working directory
    eval          Eval python code
    exec          Execute system commands
    exit          Exit the console
    help          Help menu
    history       Show command history
    quit          Exit the console
    version       Show the framework and console library version numbers

Module Commands
===============

    Command       Description
    -------       -----------
    options       Displays global options or for one or more modules
    search        Searches module names and descriptions
    show          Displays modules of a given type, or all modules
    use           Interact with a module by name or search term/index
"""
        print(info)

    def get_command_history(self):
        """Get hisoty command
        """
        for num, command in enumerate(console.command_history.get_strings()):
            print(num, command)

    def search_module(self, module):
        """Search module
        """
        n = 0
        for root, dirs, files in os.walk(self.module_path):
            for file in files:
                path = os.path.join(root, file)
                if module in path and path.split(".")[-1] == "py":
                    name = path.split(os.sep, 1)[1].replace(os.sep, "/")[:-3]
                    data = [str(n), name]
                    self.matching_modules_dict["data"].append(data)
                    n += 1
        if self.matching_modules_dict["data"]:
            self.rich_print_table(self.matching_modules_dict)
        else:
            print(colored("[-]", "red") + " No results from search")

    def chdir(self, dir_):
        """Choose dir
        """
        os.chdir(dir_)

    def options(self, option=None):
        """Show options
        """
        if not option:
            self.rich_print_table(self.global_options_dict)

    def set_command(self, key_raw, value):
        """Set key => value
        """
        key = key_raw.lower()
        if key == "prompt":
            prompt = value
        elif key == "promptchar":
            prompt_char = value

        print(key_raw, "=>", value)


    def use_module(self, module):
        """Use module
        """
        if module.isdigit():
            num = int(module)
            if num >= len(self.matching_modules_dict["data"]):
                print(colored("[-]", "red") + " Invalid module index: {}".format(num))
                return
            module = self.matching_modules_dict["data"][num][1]
        logging.debug("Use module => {}".format(module))

        # abspath = os.path.join(module_path, module+".py")
        module_import = "modules" + "." + module.replace("/", ".")
        try:
            used_module = import_module(module_import)
            used_module.main()
            # used_module.Module().console()
        except ModuleNotFoundError:
            print(colored("[-]", "red") + " Failed to load module: {}".format(module)) 


    def show_info(self, info):
        """Show info
        """
        if info == "options":
            self.options()
        elif info == "version":
            self.show_version()


    def show_version(self):
        """Get framework version
        """
        print("Framework:", __version__)
        print("Console:", __version__)


    def exec_system_command(self, command):
        """Exec system command
        """
        os.system(command)


    def eval_code(self, code):
        """Exec python code
        """
        exec(code)

    def rich_print_table(self, info_dict):
            """Show table
            """
            title = info_dict["title"]

            column_list = info_dict.get("columns")

            datas = info_dict.get("data")

            table = Table(**title)

            for column in column_list:
                table.add_column(**column)

            for data in datas:
                table.add_row(*data)

            console = Console()
            console.print(table)

    #-------------------------------Parser-------------------------------

    def parse_command(self, command_raw):
        """Parse command
        """
        command = command_raw.lower()
        if command == "":
            return None
        elif command == "cd":
            return self.chdir
        elif command == "eval":
            return self.eval_code
        elif command == "exec":
            return self.exec_system_command
        elif command == "exit" or command == "quit":
            sys.exit(0)
        elif command == "help" or command == "?":
            return self.help
        elif command == "history":
            return self.get_command_history
        elif command == "options":
            return self.options
        elif command == "search":
            return self.search_module
        elif command == "set":
            return self.set_command
        elif command == "use":
            return self.use_module
        elif command == "version":
            return self.show_version
        elif command == "show":
            return self.show_info

        print(colored("[-]", "red") + " Unknown command: " + command)

    def parse_input(self, content_raw):
        """Parse console input content
        """
        logging.debug("Content_raw => {}".format(content_raw))
        content_split = re.sub(" +", " ", content_raw).split(" ", 1)
        content_split = tuple(filter(lambda x:x!="", content_split))
        if not content_split: return(None, None)
        command_raw = content_split[0]

        command = self.parse_command(command_raw)
        if not command: return (None, None)
        command_name = command.__code__.co_name
        command_arg_count = command.__code__.co_argcount - 1

        if command_arg_count < 1:
            logging.debug("Command is {}".format(command_name))
            return (command, None)

        default_parameters = command.__defaults__

        if len(content_split) == 2:
            args = content_split[1].split(" ", command_arg_count-1)
            args_count = len(args)
        else:
            args = []
            args_count = 0

        # Minus default parameters.
        if default_parameters:
            default_arg_count = len(default_parameters)
            required_arg_count = command_arg_count - default_arg_count
        else:
            required_arg_count = command_arg_count

        if args_count < required_arg_count or args_count > command_arg_count:
            print(colored("[-]", "red") + " Argument required. Args is {}".format(args))
            print(colored("[*]", "blue") + " Required parameter count is {}".format(required_arg_count))
            print(colored("[*]", "blue") +
                " Parameters name for the {command_name} command are: {args_name}".format(
                        command_name=command_name,
                        args_name=", ".join(inspect.getfullargspec(command).args[1:])
                    )
                )
            return (None, None)

        logging.debug("Funcion is {}, Args is {}".format(command_name, args))
        return (command, args)