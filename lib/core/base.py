# -*- coding:utf-8 -*-
import warnings

from rich import box
from colorama import init
from multidict import CIMultiDict
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import NestedCompleter

from lib.config import __platform__, __version__

if __platform__ == "Windows":
    init()

warnings.filterwarnings('ignore')

class BaseInterpreter(object):
    """docstring for BaseInterpreter"""
    def __init__(self):
        super(BaseInterpreter, self).__init__()
        
        self.command_history = InMemoryHistory()
        self.prompt_session = PromptSession(history=self.command_history)

        self.prompt = "Kawaii"
        self.using_module = ""
        self.prompt_char = ">"
        self.module_path = "modules"

        self.global_options_dict = dict()
        self.global_options_dict["title"] = {
            "title": "Global Options",
            "show_header": True,
            "style": "bold",
            "box": box.MINIMAL_DOUBLE_HEAD
        }
        self.global_options_dict["columns"] = [{
                "header": "Option",
            },{
                "header":"Current Setting",
            },{
                "header":"Description",
            }
        ]
        self.global_options_dict["data"] = CIMultiDict()

        self.global_options_dict["data"]["Prompt"] = {"default": "Kawaii", "description": "The prompt string"},
        self.global_options_dict["data"]["PromptChar"] = {"default": ">", "description": "The prompt character"}
        
        
        self.completer = NestedCompleter.from_nested_dict({
            "set": {data[0]:None for data in self.global_options_dict["data"]},
            "show": {
                "version": None,
                "options": None,
            },
            "cd": None,
            "eval": None,
            "exec": None,
            "exit": None,
            "quit": None,
            "help": None,
            "?": None,
            "history": None,
            "search": None,
            "options": None,
            "use": None
        })

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
            "data": {}, 
        }