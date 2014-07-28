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
        attempts = 0
        while attempts < 10:
            try:
                response = self.__cli_browser_opener.open(self.__requestedURL)
                self.__responseContent = response.read()
                return self.__responseContent
            except urllib2.URLError as e:
                if attempts < 10:
                    attempts += 1
                    print "attempting ..."
                else:
                    print e.errno, ' ', e.filename, ' ', e.message, ' ', e.reason, ' ', e.strerror

    def parseResponse(self, _response):
        #<h3\s?class="repolist-name">\n\s*<a\s?href="(.*)"\s
        #<h3\s?class="repolist-name">\n\s*<a\s?href="(.*)"\s.+\s*.+\s?\n*.+\n*\s*<p.+\n*\s*(.+?)\n
        repositories = re.findall(r'<h3\s?class="repolist-name">\n\s*<a\s?href="(.*)"\s.+\s*.+\s?\n*.+\n*\s*(<p\sclass="description css-truncate-target">\n\s*(.+?)\n|)', _response, re.IGNORECASE)
        return repositories

    def parsePagination(self, _response=None):
        if _response is None:
            _response = self.__responseContent

        pages = re.findall(r'href="/search\?p=(.+?)&', _response, re.IGNORECASE)
        if len(pages) > 0:
            return pages[:-1]

        return None

    def getCurrentPage(self):
        try:
            currentPage = re.search(r'class="current">(.?)<', self.__responseContent, re.IGNORECASE).group(1)
            return currentPage
        except AttributeError as e:
            return None

    def enablePagination(self, _decision):
        self.__pagination = _decision

    def parseVersions(self, _res):
        #<span class="tag-name">(.+?)</span>
        #tags\?after=
        return re.findall(r'<span class="tag-name">(.+?)</span>', _res, re.IGNORECASE)

    def __isStillMore(self, _response):
        return re.search(r'tags\?after=', _response, re.IGNORECASE)

    def getPackageVersions(self, _response):
        versions = []
        versions.extend(self.parseVersions(_response))
        while self.__isStillMore(_response):
            self.setRequestedURL(self.getRequestedURL()+'?after='+versions[-1])
            _response = self.submit()
            versions.extend(self.parseVersions(_response))

        return versions
    """
    def testing(self):
        #<p class="description css-truncate-target">\n*\s*(.+?)\s*\n*</p>
        return re.findall(r'<p class="description css-truncate-target">\n*\s*(.+?)\s*\n*</p>', self.__responseContent, re.IGNORECASE)
    """
    def closeConnections(self):
        self.__cli_browser_opener.close()

#https://github.com/angular/angular.js/tags
"""
browser = cli_browser()
browser.setRequestedURL('https://github.com/dsel/dsel.github.io/tags')
response = browser.submit()

v = browser.getPackageVersions(response)
browser.closeConnections()
import pprint
print pprint.pprint(v, indent=4)
print len(v)
"""
"""
hn = open('test.html', "w")
hn.write(response)
hn.close()"""