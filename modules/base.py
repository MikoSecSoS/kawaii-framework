# -*- coding:utf-8 -*-

from prompt_toolkit.completion import NestedCompleter
from multidict import CIMultiDict
from rich import box

from lib.core.console import KawaiiInterpreter
from lib.utils.log import lprint, colored

class BaseModule(KawaiiInterpreter):
    """docstring for BaseModule"""
    def __init__(self):
        super(BaseModule, self).__init__()
    
    def initialization(self, data):
        self.global_options_dict["title"] = {
                "title": "Module options ({})".format(self.using_module),
                "show_header": True,
                "style": "bold",
                "box": box.MINIMAL_DOUBLE_HEAD
            }
        self.global_options_dict["columns"] = [{
                    "header": "Name",
                },{
                    "header":"Current Setting",
                },{
                    "header":"Required",
                },{
                    "header":"Description",
                }
            ],
        self.global_options_dict["data"] = CIMultiDict()
        for k,v in data.items():
            self.global_options_dict["data"][k] = v
        
        options = self.completer.options
        options["set"] = {data[0]:None for data in self.global_options_dict["data"]}
        self.completer = NestedCompleter.from_nested_dict(options)

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

Exploit Commands
================

    Command       Description
    -------       -----------
    exploit       Launch an exploit attempt
    run           Alias for exploit
"""
        print(info)

    def check_options(self):
        data = self.global_options_dict["data"]
        for d in data:
            if d[2].lower() == "yes" and d[1] == "":
                lprint("error",  "Not set " + colored(d[0], "green"))
                return False
        return True

    def parse_command(self, command_raw):
        """Parse command
        """
        command = command_raw.lower()
        if command == "":
            return None
        elif command == "cd":
            return self.chdir
        elif command == "debug":
            return self.debug
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
        elif command == "exploit" or command == "run":
            return self.run

        lprint("error", "Unknown command: " + command)

    def run(self, exploit):
        check_out = self.check_options()
        if check_out:
            exploit()