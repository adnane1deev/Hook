__author__ = 'Adnane Deev'

import re
import urllib2
import cookielib


class cli_browser(object):

    def __init__(self):
        self.__cookies = cookielib.CookieJar()
        self.__cookiesHandler = urllib2.HTTPCookieProcessor(self.__cookies)

        self.__cli_browser_opener = urllib2.build_opener(self.__cookiesHandler)
        urllib2.install_opener(self.__cli_browser_opener)

        self.__userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
        self.__cli_browser_opener.addheaders = [('User-agent', self.__userAgent)]
        self.__requestedURL = None
        self.__pagination = False
        self.__responseContent = None

    def getHttpConnection(self):
        return self.__cli_browser_opener

    def setUserAgent(self, _userAgent):
        self.__userAgent = _userAgent
        self.__cli_browser_opener.addheaders = [('User-agent', self.__userAgent)]

    def getUserAgent(self):
        return self.__userAgent

    def setRequestedURL(self, _requestedURL):
        self.__requestedURL = _requestedURL

    def getRequestedURL(self):
        return self.__requestedURL

    def submit(self):
        response = self.__cli_browser_opener.open(self.__requestedURL)
        self.__responseContent = response.read()
        return self.__responseContent

    def parseResponse(self, _response):
        repositories = re.findall(r'<h3\s?class="repolist-name">\n\s*<a\s?href="(.*)"\s', _response, re.IGNORECASE)
        return repositories

    def parsePagination(self, _response=None):
        if _response is None:
            _response = self.__responseContent

        pages = re.findall(r'href="/search\?p=(.+?)&', _response, re.IGNORECASE)
        return pages

    def getCurrentPage(self):
        currentPage = re.search(r'class="current">(.?)<', self.__responseContent, re.IGNORECASE).group(1)
        return currentPage

    def enablePagination(self, _decision):
        self.__pagination = _decision

    def closeConnections(self):
        self.__cli_browser_opener.close()