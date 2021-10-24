# -*- coding:utf-8 -*-

import copy
import os
import sys
from base64 import b64encode
from html import unescape

import requests
from faker import Faker
from prompt_toolkit.completion import NestedCompleter
from rich import box
from termcolor import colored

from lib.core.console import KawaiiInterpreter


class FofaSearch(KawaiiInterpreter):
    """docstring for FofaSearch"""

    def __init__(self):
        super(FofaSearch, self).__init__()
        module_type, module_path = __file__.split(self.module_path + os.sep)[-1].replace(".py", "").split(os.sep, 1)
        using_module = " {module_type}({module_path}) ".format(
            module_type=module_type,
            module_path=colored(module_path.replace(os.sep, "/"), "red")
        )
        self.using_module = using_module
        # ----------------------------------------------------------------------------
        self.CONTENT = ""
        self.AUTH = ""
        self.EMAIL = ""
        self.FILE = ""
        self.KEY = ""
        self.MODE = "none"
        self.PAGE = "1"
        self.PAGESIZE = "10"
        self.PASSWORD = ""
        self.UA = self.flag
        # ----------------------------------------------------------------------------
        self.fofa_search_url = "https://api.fofa.so/v1/search"
        self.session = requests.Session()
        self.session.headers = {"User-Agent": self.UA}
        # ----------------------------------------------------------------------------

        self.global_options_dict = {
            "title": {
                "title": "Module options ({})".format(self.using_module),
                "show_header": True,
                "style": "bold",
                "box": box.MINIMAL_DOUBLE_HEAD
            },
            "columns": [{
                "header": "Name",
            }, {
                "header": "Current Setting",
            }, {
                "header": "Required",
            }, {
                "header": "Description",
            }
            ],
            "data": [
                ["AUTH", self.AUTH, "No", "Fofa Authorization"],
                ["CONTENT", self.CONTENT, "Yes", "Fofa search content"],
                ["EMAIL", self.EMAIL, "No", "Fofa email"],
                ["FILE", self.FILE, "No", "Fofa search output file.(csv)"],
                ["KEY", self.KEY, "No", "Fofa key"],
                ["MODE", self.MODE, "Yes", "Login fofa mode(none, auth, account, api)"],
                ["PAGE", self.PAGE, "Yes", "Fofa search page"],
                ["PAGESIZE", self.PAGESIZE, "No", "Fofa search result size.(10, 20)"],
                ["PASSWD", self.PASSWORD, "No", "Fofa password"],
                ["UA", self.UA, "No", "Request User-Agent(random)"],
            ]
        }
        options = copy.deepcopy(self.completer.options)
        options["set"] = {data[0]: None for data in self.global_options_dict["data"]}
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

    def update_init(self):
        self.global_options_dict["data"] = [
            ["AUTH", self.AUTH, "No", "Fofa Authorization"],
            ["CONTENT", self.CONTENT, "Yes", "Fofa search content"],
            ["EMAIL", self.EMAIL, "No", "Fofa email"],
            ["FILE", self.FILE, "No", "Fofa search output file.(csv)"],
            ["KEY", self.KEY, "No", "Fofa key"],
            ["MODE", self.MODE, "Yes", "Login fofa mode(none, auth, account, api)"],
            ["PAGE", self.PAGE, "Yes", "Fofa search page"],
            ["PAGESIZE", self.PAGESIZE, "No", "Fofa search result size.(10, 20)"],
            ["PASSWD", self.PASSWORD, "No", "Fofa password"],
            ["UA", self.UA, "No", "Request User-Agent(random)"],
        ]

    def set_command(self, key_raw, value):
        key = key_raw.lower()
        if key == "prompt":
            self.prompt = value
        elif key == "prompt_char":
            self.prompt_char = value
        elif key == "content":
            self.CONTENT = value
        elif key == "auth":
            self.AUTH = value
            self.session.headers["Authorization"] = self.AUTH
        elif key == "email":
            self.EMAIL = value
        elif key == "key":
            self.KEY = value
        elif key == "mode":
            self.MODE = value
        elif key == "file":
            self.FILE = value
        elif key == "page":
            self.PAGE = value
        elif key == "pagesize":
            self.PAGESIZE = value
        elif key == "passwd":
            self.PASSWORD = value
        elif key == "ua":
            if value == "random":
                fake = Faker()
                self.UA = fake.ua
                self.session.headers["User-Agent"] = self.UA

        self.update_init()
        print(key_raw, "=>", value)

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

        print(colored("[-]", "red") + " Unknown command: " + command)

    def check_options(self):
        data = self.global_options_dict["data"]
        for d in data:
            if d[2].lower() == "yes" and d[1] == "":
                print(colored("[-]") + " Not set " + colored(d[0], "green"))
                return False
        return True

    def parse_json_data(self, data_raw):
        if not data_raw.get("data"):
            print(colored("[-]", "red") + " Parse_json_data Error: {}".format(data_raw.get("message")))
            return

        data_assets = data_raw["data"].get("assets", [])
        for asset in data_assets:
            host = asset.get("host", "")
            title = unescape(asset.get("title").strip())
            link = asset.get("link", "")
            ip = asset.get("ip", "")
            port = str(asset.get("port", ""))
            domain = asset.get("domain", "")
            base_protocol = asset.get("base_protocol", "")
            protocol = asset.get("protocol", "")
            protocol = protocol if protocol else base_protocol
            server = asset.get("server", "")
            type_ = asset.get("type", "")

            data_dict = {
                "HOST": host,
                "标题": title,
                "链接": link,
                "IP地址": ip,
                "端口": port,
                "域名": domain,
                "协议": protocol,
                "服务指纹": server,
                "类型": type_,
            }

            yield data_dict

    def exploit(self):
        print(colored("[*]", "blue") + " Module started successfully")

        isPage = lambda n: int(n) + 1 if n.isdigit() else 0

        columns = []
        datas = []

        qbase64 = b64encode(self.CONTENT.encode()).decode()
        pn = isPage(self.PAGE)
        for pn in range(1, pn):
            print(colored("[*]", "blue") + " Search fofa page => {}".format(pn))
            params = {
                'q': self.CONTENT,
                'qbase64': qbase64,
                'full': 'true',
                'pn': pn,
                'ps': self.PAGESIZE
            }
            req = self.session.get(self.fofa_search_url, params=params)
            data_yield = self.parse_json_data(req.json())
            for data in data_yield:
                if not columns:
                    for key in data.keys():
                        columns.append({
                            "header": key,
                            "justify": "center",
                            "overflow": "ignore"
                        })
                if data:
                    datas.append(list(data.values()))

        print(colored("[*]", "blue") + " Search done.")

        if not datas:
            return
        datas_dict = {
            "title": {
                "title": "",
                "show_header": True,
                "style": "bold",
                "box": box.HEAVY_HEAD
            },
            "columns": columns,
            "data": datas
        }
        self.rich_print_table(datas_dict)

    def run(self):
        check_out = self.check_options()
        if check_out:
            self.exploit()


def main():
    fofasearch = FofaSearch()
    fofasearch.console()
