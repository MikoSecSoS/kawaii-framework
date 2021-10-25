# -*- coding: utf-8 -*-
from gevent import monkey
def stub(*args, **kwargs):  # pylint: disable=unused-argument
    pass
monkey.patch_all = stub
import requests
import grequests

from lib.config import __framework__, __version__

from tqdm import tqdm

class ProgressSession(object):
    def __init__(self, pn, session, bar=True):
        self.bar = bar
        self.pbar = tqdm(total = pn, desc = 'Making async requests')
        self.sess = session
    def update(self, r, *args, **kwargs):
        if not r.is_redirect:
            self.pbar.update()
    def __enter__(self):
        self.sess.hooks['response'].append(self.update)
        return self.sess
    def __exit__(self, *args):
        if self.bar:
            self.pbar.close()

class HEADERS(object):
    UA = __framework__ + " " + __version__
