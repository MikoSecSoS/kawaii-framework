# -*- coding: utf-8 -*-

from lib.core.base import BaseInterpreter
from lib.core.parser import Parser

from prompt_toolkit import ANSI

class KawaiiInterpreter(Parser):
    """docstring for KawaiiInterpreter"""
    def __init__(self):
        super(KawaiiInterpreter, self).__init__()

    def console(self):
        while 1:
            try:
                prompt_list = [i for i in (self.prompt, self.using_module, self.prompt_char) if i]
                prompt_text = " ".join(prompt_list)+" "
                content = self.prompt_session.prompt(ANSI(prompt_text), completer=self.completer)
                if content == "q": exit()
                input_yield = self.parse_input(content)
                for func, args in input_yield:
                    if func:
                        if args:
                            func(*args)
                        else:
                            func()
            except KeyboardInterrupt:
                print("KeyboardInterrupt: use the 'exit' command to quit")
            except Exception as e:
                raise e
