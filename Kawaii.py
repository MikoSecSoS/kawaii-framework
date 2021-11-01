#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import sys

from lib.core.console import KawaiiInterpreter
from lib.config import __banner__

module_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, module_path)

def main():
    print(__banner__)
    KawaiiInterpreter().console()

if __name__ == '__main__':
    main()