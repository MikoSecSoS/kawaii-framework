# -*- coding: utf-8 -*-

import inspect

from rich.console import Console

from termcolor import colored

console = Console()

def lprint(level, *args):
    """Log print"""
    level_upper = level.upper()
    if level_upper == "INFO":
        console.print("[green][*]", str(*args))
    elif level_upper == "WARN":
        console.print("[yellow][-]", str(*args))
    elif level_upper == "ERROR":
        console.print("[red][!]", str(*args))
    elif level_upper == "DEBUG":
        now_time = str(datetime.now()).split(".")[0]
        extract_stack = traceback.extract_stack()[-2]
        stack_info = "{extract_stack.filename} line {extract_stack.line} in {extract_stack.name}"
        console.print(f"[{now_time}] <{stack_info}> [cyan]DEBUG - ", str(*args))
    else:
        console.print(level, *args)