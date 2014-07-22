__author__ = 'Adnane Deev'

import types
import pprint as pn
from cli_browser import cli_browser


class idm_exception(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class download_manager(object):

    def __init__(self):
        self.__types = {'application/zip': 'zip', 'application/rar': 'rar'}
        self.__URLS = []
        self.__URL = ''
        self.__browser = None

    def setURL(self, _url):
        self.__URL = _url

    def setURLS(self, _urls):
        self.__URLS.extend(_urls)

    def addURL(self, _url):
        self.__URLS.append(_url)

    def __download(self, _url):
        file_size = None
        file_name = ""
        http_connection = None
        file_handler = None

        while file_size is None:
            http_connection = self.__browser.open(_url)
            metadata = http_connection.info()
            print pn.pprint(metadata.dict, indent="2")
            file_name = _url.split('/')[-4]+"-"+_url.split('/')[-3]+"."+self.__types[metadata.getheaders("content-type")[0]]
            file_handler = open(file_name, 'wb')
            #print metadata.getheaders("Content-Type")
            #print metadata.dict
            try:
                file_size = int(metadata.getheaders("Content-Length")[0])
            except Exception:
                print "Couldn't resolve the URL: trying again ..."

        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192

        while True:
            __buffer = http_connection.read(block_sz)
            if not __buffer:
                break

            file_size_dl += len(__buffer)
            file_handler.write(__buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status += chr(8)*(len(status)+1)
            print status,

        file_handler.close()
        print

    def startQueue(self, _url_s):
        try:
            if isinstance(_url_s, types.ListType):
                print 'list'
                for url in _url_s:
                    self.__download(url)

            elif isinstance(_url_s, types.StringType):
                print 'str'
                self.__download(_url_s)

            else:
                raise idm_exception('sss')
        except idm_exception as e:
            print e.value

    def plugInBrowserWithDownloadManager(self, _browser):
        self.__browser = _browser

"""
    Testing if it functions as required
"""

urls = ["https://github.com/bower/registry/archive/master.zip",
        "https://github.com/bower/bower/archive/master.zip",
        "https://github.com/zendframework/ZendSkeletonApplication/archive/master.zip"]

browserObject = cli_browser()
browserConnection = browserObject.getHttpConnection()
downloadManager = download_manager()
downloadManager.chaineBrowserConnection(browserConnection)
downloadManager.startQueue(urls)

browserConnection.close()
browserObject.closeConnections()