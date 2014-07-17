__author__ = 'Asus'

import re
import urllib2
import cookielib


class cli_browser(object):

    def __init__(self):
        self.cookies = cookielib.CookieJar()
        cookiesHandler = urllib2.HTTPCookieProcessor(self.cookies)

        self.cli_browser_opener = urllib2.build_opener(cookiesHandler)
        urllib2.install_opener(self.cli_browser_opener)

        self.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
        self.cli_browser_opener.addheaders = [('User-agent', self.userAgent)]
        self.requestedURL = None
        self.pagination = False
        self.responseContent = None

    def setUserAgent(self, __userAgent):
        self.userAgent = __userAgent
        self.cli_browser_opener.addheaders = [('User-agent', self.userAgent)]

    def getUserAgent(self):
        return self.userAgent

    def setRequestedURL(self, __requestedURL):
        self.requestedURL = __requestedURL

    def getRequestedURL(self):
        return self.requestedURL

    def submit(self):
        response = self.cli_browser_opener.open(self.requestedURL)
        self.responseContent = response.read()
        return self.responseContent

    def parseResponse(self, __response):
        repositories = re.findall(r'<h3\s?class="repolist-name">\n\s*<a\s?href="(.*)"\s', __response, re.IGNORECASE)
        return repositories

    def parsePagination(self, __response=None):
        if __response is None:
            __response = self.responseContent

        pages = re.findall(r'href="/search\?p=(.+?)&', __response, re.IGNORECASE)
        return pages

    def getCurrentPage(self):
        currentPage = re.search(r'class="current">(.?)<', self.responseContent, re.IGNORECASE).group(1)
        return currentPage

    def enablePagination(self, __decision):
        self.pagination = __decision