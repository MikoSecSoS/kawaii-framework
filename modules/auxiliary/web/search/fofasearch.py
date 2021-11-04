# -*- coding:utf-8 -*-

import os
import sys

from base64 import b64encode
from html import unescape

from faker import Faker

from lib.utils.log import lprint, colored
from lib.file import save2csv
from lib.request import grequests, requests, ProgressSession, HEADERS
from modules.base import BaseModule

class FofaSearch(BaseModule):
    """docstring for FofaSearch"""

    def __init__(self):
        super(FofaSearch, self).__init__()
        module_type, module_path = __file__.split(self.module_path+os.sep)[-1].replace(".py", "").split(os.sep, 1)
        using_module = "{module_type}({module_path})".format(
                                        module_type=module_type,
                                        module_path=colored(module_path.replace(os.sep, "/"), "red")
                                    )
        self.using_module = using_module
        #---------------------------Module variable----------------------------------
        self.fofa_search_url = "https://api.fofa.so/v1/search"
        self.fofa_key_searh_url = "https://fofa.so/api/v1/search/all"
        self.session = requests.Session()
        self.session.headers["User-Agent"] = HEADERS.UA
        #----------------------------------------------------------------------------
        
        self.initialization({
            "AUTH": {"default": "", "required": "No", "description": "Fofa Authorization"},
            "CONTENT": {"default": "", "required": "Yes", "description": "Fofa search content"},
            "EMAIL": {"default": "", "required": "No", "description": "Fofa email"},
            "FILE": {"default": "", "required": "No", "description": "Output file.(.csv)"},
            "FIELDS": {"default": "host,title,ip,domain,port,protocol,server,fid", "required": "No", "description": "Fofa api fields"},
            "FULL": {"default": "false", "required": "No", "description": "Fofa search show full(true/false)"},
            "KEY": {"default": "", "required": "No", "description": "Fofa key"},
            "MODE": {"default": "none", "required": "Yes", "description": "Login fofa mode(none, auth, account, api)"},
            "PAGE": {"default": "0", "required": "Yes", "description": "Fofa search page"},
            "PAGESIZE": {"default": "10", "required": "Yes", "description": "Fofa search result size."},
            "PASSWD": {"default": "", "required": "No", "description": "Fofa password"},
            "UA": {"default": HEADERS.UA, "required": "Yes", "description": "Request User-Agent(random)"},
        })


    def parse_json_data(self, data_raw, get_total_count=False):
        if self.MODE != "api":
            if not data_raw.get("data"):
                lprint("error", "Parse_json_data Error: {}".format(data_raw.get("message")))
                return

            if get_total_count:
                if not data_raw["data"].get("page"):
                    lprint("error", "Parse_json_data Error: {}".format(data_raw.get("message")))
                    return
                else:
                    yield data_raw["data"]["page"].get("total")
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
        else:
            if get_total_count:
                if not data_raw.get("size"):
                    lprint("error", "Parse_json_data Error: {}".format(data_raw.get("message")))
                    return
                yield data_raw.get("size")
                return
            if not data_raw.get("results"):
                lprint("error", "Parse_json_data Error: {}".format(data_raw.get("message")))
                return
            fields_upper = [field.upper() for field in self.FIELDS.split(",")]
            results = data_raw["results"]
            for result in results:
                data_dict = {k:v for k,v in zip(fields_upper, result)}
                yield data_dict

    def get_result_total_count(self, qbase64):
        if self.MODE != "api":
            params = {
                "q": self.CONTENT,
                "qbase64": qbase64,
                "full": self.FULL,
                "pn": "1",
                "ps": self.PAGESIZE
            }
            req = self.session.get(self.fofa_search_url, params=params)
            return next(self.parse_json_data(req.json(), get_total_count=True))
        else:
            params = {
                "email": self.EMAIL,
                "key": self.KEY,
                "qbase64": qbase64,
                "full": self.FULL,
                "page": "1",
                "size": self.PAGESIZE,
                "fields": self.FIELDS
            }
            req = self.session.get(self.fofa_key_searh_url, params=params)
            return next(self.parse_json_data(req.json(), get_total_count=True))

    def fofa_search(self, qbase64, pn):
        if pn == 1:
            return
        with ProgressSession(pn-1, self.session) as sess:
            req_list = []
            for pn in range(1, pn):
                if self.MODE != "api":
                    params = {
                        "q": self.CONTENT,
                        "qbase64": qbase64,
                        "full": self.FULL,
                        "pn": pn,
                        "ps": self.PAGESIZE
                    }
                    req = grequests.get(self.fofa_search_url, params=params, session=sess)
                else:
                    params = {
                        "email": self.EMAIL,
                        "key": self.KEY,
                        "qbase64": qbase64,
                        "full": self.FULL,
                        "page": pn,
                        "size": self.PAGESIZE,
                        "fields": self.FIELDS
                    }
                    req = grequests.get(self.fofa_key_searh_url, params=params, session=sess)

                req_list.append(req)
            res_list = grequests.map(req_list)
            for res in res_list:
                if res:
                    yield self.parse_json_data(res.json())

    def exploit(self):
        lprint("info", "Module started successfully.")

        qbase64 = b64encode(self.CONTENT.encode()).decode()

        total_count = self.get_result_total_count(qbase64)

        max_page = int(total_count/int(self.PAGESIZE))+1

        lprint("info", "Result total count is {}".format(total_count))
        lprint("info", "Max page is {}".format(max_page))

        if int(self.PAGE) > max_page:
            lprint("info", "The number of pages set is greater than the total number of results.")
            lprint("info", "Set page is {}".format(max_page))

            self.PAGE = max_page
            self.update_options_data()

        isPage = lambda n: int(n)+1 if n.isdigit() else 0

        pn = isPage(self.PAGE)

        if not pn:
            lprint("error", "PAGE => `{}` not is number.".fotmat(self.PAGE))
            return

        result = self.fofa_search(qbase64, pn)
        datas = []
        columns = []

        lprint("info", "Search done.")

        for data_yield in result:
            for data in data_yield:
                if not columns:
                    for key in data.keys():
                        columns.append({
                            "header": key,
                            "justify": "center",
                            "overflow": "ignore"
                        })
                datas.append(list(data.values()))

        if not datas:
            lprint("error", "Search result is null.")
            return

        datas_dict = {
            "title": {
                "title": "",
                "show_header": True,
                "style": "bold",
                "box": box.HEAVY_HEAD
            },
            "columns": list(columns),
            "data": list(datas)
        }
        if self.FILE.lower().endswith(".csv"):
            save2csv(self.FILE, [col["header"] for col in columns], datas)
        self.rich_print_table(datas_dict)


def main():
    fofasearch = FofaSearch()
    fofasearch.console()