# -*- coding:utf-8 -*-

from lib.config import __platform__, __version__, __prompt__

from importlib import import_module

from rich import box
from colorama import init
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import NestedCompleter

if __platform__ == "Windows":
    init()

class BaseInterpreter(object):
    """docstring for BaseInterpreter"""
    def __init__(self):
        super(BaseInterpreter, self).__init__()
        
        self.command_history = InMemoryHistory()
        self.prompt_session = PromptSession(history=self.command_history)

        self.prompt = __prompt__
        self.using_module = " "
        self.prompt_char = ">"
        self.flag = "Kawaii-Framework " + __version__
        self.module_path = "modules"

        self.matching_modules_dict = {
            "title": {
                "title": "Matching Modules",
                "show_header": True,
                "style": "bold",
                "box": box.MINIMAL_DOUBLE_HEAD
            },
            "columns": [{
                    "header": "#",
                },{
                    "header":"Name",
                }
            ],
            "data": [
            ], 
        }

