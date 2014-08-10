#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import cookielib
import os_operations as op
import sys


def robot():
    return """
     [00]
    /|__|\\
      ''
    """


class cli_browser(object):

    def __init__(self):
        self.__http_status_code = {
            200: 'Ok',
            201: 'CREATED',
            202: 'Accepted ',
            203: 'Partial Information',
            204: 'No Response',
            400: 'Bad request',
            401: 'Unauthorized',
            402: 'PaymentRequired',
            403: 'Forbidden',
            404: 'Not found',
            500: 'Internal Error',
            501: 'Not implemented',
            502: 'Service temporarily overloaded',
            503: 'Gateway timeout',
            301: 'Moved',
            302: 'Found',
            303: 'Method',
            304: 'Not Modified'
        }

        self.__cookies = cookielib.CookieJar()
        self.__cookiesHandler = urllib2.HTTPCookieProcessor(self.__cookies)

        self.__cli_browser_opener = urllib2.build_opener(self.__cookiesHandler)
        urllib2.install_opener(self.__cli_browser_opener)

        self.__userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
        self.__cli_browser_opener.addheaders = [('User-agent', self.__userAgent)]
        self.__requestedURL = None
        self.__pagination = False
        self.__responseContent = None
        self.__bots_verified = True
        self.__first_round = True

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

    def status_code_desc(self, _code):
        try:
            return self.__http_status_code[_code]
        except Exception:
            return 'Not found'

    def submit(self, _return_status_code=False):
        attempts = 0
        while attempts < 10:
            try:
                response = self.__cli_browser_opener.open(self.__requestedURL)
                self.__responseContent = response.read()
                self.__bots_verified = True
                if 0 < attempts <= 10 and self.__first_round:
                    print "\n"

                self.__first_round = True
                return self.__responseContent
            except urllib2.URLError as e:
                if _return_status_code:
                    return e.code

                if self.__bots_verified:
                    print robot()

                self.__bots_verified = False

                if attempts < 10:
                    attempts += 1

                    status = "\r\tChecking for bots %s" % (self.gen(attempts))
                    #print status,
                    sys.stdout.write(status)
                    sys.stdout.flush()

                else:
                    print e.errno, ' ', e.filename, ' ', e.message, ' ', e.strerror

        if attempts == 10:
            self.__first_round = False
        #print
        return None

    def gen(self, t):
        m = 10 - t
        str = '[{0}{1}]'.format(("#" * t), ("-" * m))
        return str

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

    def getCurrentPage(self, _res=None):
        try:
            if _res is None:
                _res = self.__responseContent
            currentPage = re.search(r'class="current">(.+?)<', _res, re.IGNORECASE).group(1)
            return currentPage
        except AttributeError as e:
            return 1

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
