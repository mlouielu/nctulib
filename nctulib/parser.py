# -*- coding: utf-8 -*-
#
# This is the parser of exlibris primo library search system, it aim to provide
# the ability to parse different exlibris primo library search system, not only
# for NCTU.
#

import urllib.parse
import requests
from lxml import etree


class EXLLocation:
    # A location of EXL

    def __init__(self, e):
        # Input is a lxml element represent div[@class="EXLLocationList"]
        self.library = e.xpath('descendant::span/span')[0].text.strip()
        self.floor = e.xpath('descendant::span[3]/strong')[0].text
        self.cite = e.xpath('descendant::span[3]/cite')[0].text
        self.available = e.xpath('descendant::span[3]/em')[0].text

    def __repr__(self):
        return f'<{self.library}: {self.cite}: {self.available}>'

    def json(self):
        return {
            'library': self.library,
            'floor': self.floor,
            'cite': self.cite,
            'available': self.available
        }


class EXLItem:
    """This represent a item in Primo
    """

    def __init__(self, item, baseurl=''):
        # item: lxml etree element for EXLResult
        self.title = ''.join(item.xpath('descendant::h2/a')[0].itertext()).strip()
        self.author = ''.join(item.xpath('descendant::h3')[0].itertext()).strip() if item.xpath('descendant::h3') else None
        self.url = item.xpath('descendant::h2/a')[0].get('href')
        self.url = ('' if self.url.startswith('http') else baseurl) + self.url
        self.url = self.url.replace('detailsTab', 'locationsTab')
        self.bid = urllib.parse.parse_qs(self.url)['doc'][-1]
        self.image = item.xpath('descendant::img')[0].get('src')

    def get_locations(self):
        LOCATION_URL = ('http://ustcate.lib.nctu.edu.tw/primo_library/libweb/'
                        f'action/display.do?tabs=locationsTab&fn=search&doc={self.bid}')
        r = requests.get(LOCATION_URL)
        root = etree.HTML(r.text)

        return [EXLLocation(self.bid).json() for e in root.xpath('//div[@class="EXLLocationList"]')]

    def json(self):
        return {
            'title': self.title,
            'author': self.author,
            'bid': self.bid,
            'image': self.image
        }


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
