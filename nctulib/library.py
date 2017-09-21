# -*- coding: utf-8 -*-

import unicodedata
import requests
import execjs
from lxml import etree

from nctulib.parser import EXLParser


class NCTULibrary:
    BASE_URL = 'http://ustcate.lib.nctu.edu.tw/primo_library/libweb/action/'
    SEARCH_URL = BASE_URL + 'search.do?fn=search&tab=union&vid=NCTU&vl(freeText0)={q}'

    def search(self, q, title=None):
        r = requests.get(self.SEARCH_URL.format(q=q))
        p = EXLParser(r.text, baseurl=self.BASE_URL)

        return p.data
