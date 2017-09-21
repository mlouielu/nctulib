# -*- coding: utf-8 -*-
#
# This is the parser of exlibris primo library search system, it aim to provide
# the ability to parse different exlibris primo library search system, not only
# for NCTU.
#

import requests
from lxml import etree


class EXLItem:
    """This represent a item in Primo
    """

    def __init__(self, item, baseurl=''):
        # item: lxml etree element for EXLResult
        self.title = ''.join(item.xpath('descendant::h2/a')[0].itertext()).strip()
        self.author = ''.join(item.xpath('descendant::h3')[0].itertext()).strip() if item.xpath('descendant::h3') else None
        self.url = item.xpath('descendant::h2/a')[0].get('href')
        self.url = ('' if self.url.startswith('http') else baseurl) + self.url


class EXLParser:
    def __init__(self, source=None, url=None, baseurl=''):
        self.source = source
        self.baseurl = baseurl

        if url:
            url = ('' if url.startswith('http') else self.baseurl) + url
            self.source = requests.get(url).text

        self.root = etree.HTML(self.source)
        self.data = []

        self._init_data()

    def _init_data(self):
        for item in self.root.xpath('//tr[contains(@class, "EXLResult")]'):

            dedup = self.is_dedup(item)
            if dedup:
                self.data.extend(EXLParser(url=dedup, baseurl=self.baseurl).data)
            self.data.append(EXLItem(item, baseurl=self.baseurl))

    def is_dedup(self, item):
        if 'dedup' in item.xpath('descendant::h2/a')[0].get('href'):
            return item.xpath('descendant::h2/a')[0].get('href')
        return False
