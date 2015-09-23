"""

"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from lxml.html import fromstring
import requests


class PageRender(object):
    def __init__(self, url, page=None, text=str(), neron=False):
        self.url, self.page, self.text, self.neron = url, page, text, neron
        self.parse_fail = True
        self.runrequests()

    def runrequests(self):
        """Get html, links and text from original url"""
        try:
            self.page = self.simple_parse(self.url)
            self.text = ' '.join([unicode(ele.text_content().strip()) for ele in
                                  self.page.xpath('//p') if ele.text_content()])
            self.parse_fail = False
        except: pass

    # ================================
    # conveniences
    # ================================
    @staticmethod
    def simple_parse(url):
        """convenience: pass any url and it will try and text render"""
        return fromstring(requests.get(url).content)
