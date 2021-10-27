from lib.core.console import KawaiiInterpreter

from lib.utils.log import lprint, colored
from prompt_toolkit.completion import NestedCompleter

class BaseModule(KawaiiInterpreter):
    """docstring for BaseModule"""
    def __init__(self):
        super(BaseModule, self).__init__()
    
    def initialization(self, options_dict):
        self.global_options_dict = options_dict
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