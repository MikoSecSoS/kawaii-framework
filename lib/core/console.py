# -*- coding: utf-8 -*-

from lib.core.base import BaseInterpreter
from lib.core.parser import Parser
from lib.config import __platform__

from rich import box
from prompt_toolkit import ANSI
from prompt_toolkit.completion import NestedCompleter

class KawaiiInterpreter(Parser):
    """docstring for KawaiiInterpreter"""
    def __init__(self):
        super(KawaiiInterpreter, self).__init__()
        
        self.global_options_dict = {
            "title": {
                "title": "Global Options",
                "show_header": True,
                "style": "bold",
                "box": box.MINIMAL_DOUBLE_HEAD
            },
            "columns": [{
                    "header": "Option",
                },{
                    "header":"Current Setting",
                },{
                    "header":"Description",
                }
            ], 
            "data": [
                    ["Prompt", self.prompt, "The prompt string"],
                    ["PromptChar", self.prompt_char, "The prompt character"],
                ]
        }
        
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
    def console(self):
        while 1:
            try:
                prompt_text = self.prompt + self.using_module + self.prompt_char + " "
                content = self.prompt_session.prompt(ANSI(prompt_text), completer=self.completer)
                if content == "q": exit()
                func, args = self.parse_input(content)
                if func:
                    if args:
                        func(*args)
                    else:
                        func()
            except KeyboardInterrupt:
                print("KeyboardInterrupt: use the 'exit' command to quit")
            except Exception as e:
                raise e
