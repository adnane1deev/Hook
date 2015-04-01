#!/usr/bin/python
# -*- coding: utf-8 -*-

import types
import hook_system_variables as hook
import os_operations as op
import package_manager as manager
from colorama import Fore
from urllib2 import URLError

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

    def is_in_cache(self, _pkg):
        cache_path = op.get_home()+'/'+hook.data_storage_path+'/'+_pkg
        if op.is_exits(cache_path):
            return True

        return False

    def __download(self, _url, _name_size, _params=None):
        http_connection = self.__browser.open(_url)
        file_size = _name_size['file_size']
        file_name = _name_size['file_name']
        path = op.get_home()+'/'+hook.data_storage_path+'/'

        file_handler = open(path+file_name, 'wb')
        #print
        name, version = manager.package_split(file_name)
        #print "Downloading: %s (%s): %0.2fMB" % (name, version, op.to_mb(file_size))
        print "Downloading: " + Fore.GREEN + "%s (%s)" % (name, version) + Fore.RESET

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

        if not _params:
            op.decompress_zipfile(path+file_name, './components')
        else:
            op.decompress_zipfile(path+file_name, '.')

    def load_from_cache(self, file_name, file_size, _params=None):
        if self.is_in_cache(file_name):
            cache_path = op.get_home()+'/'+hook.data_storage_path+'/'+file_name

            if not _params:
                op.decompress_zipfile(cache_path, './components')
            else:
                op.decompress_zipfile(cache_path, '.')
            #print
            name, version = manager.package_split(file_name)
            #print "Downloading: %s (%s): %0.2fMB" % (name, version, op.to_mb(file_size))
            print "Downloading: " + Fore.GREEN + "%s (%s)" % (name, version) + Fore.RESET

            status = r" %10d  [%s]" % (file_size,  'Loaded from the cache')
            print status
            #print
            return False

        return True

    def __get_package_name(self, _url):
        file_size = None
        file_name = ""

        while True:
            try:
                http_connection = self.__browser.open(_url)
                metadata = http_connection.info()
                file_name = metadata.dict['content-disposition'].split('=')[1]


                file_size = int(metadata.getheaders("Content-Length")[0])
                break
            except URLError as e:
                print Fore.YELLOW + str(e.code) + Fore.RESET + ": " + _url
                return None
            except Exception:
                #print "Couldn't resolve the URL: trying again ..."
                pass

        return {'file_name': file_name, 'no_ext_name': file_name.split('.')[0], 'file_size': file_size}

    def __get_file(self, _url, _repository=None, _params=None):
        if not _params:
            _params = {'type': 'install'}

        pkg_name_size = self.__get_package_name(_url)
        if pkg_name_size is None:
            return None

        if _params['type'] == 'update' and not manager.is_package_registered(pkg_name_size['file_name']):
            if manager.is_in_cache(pkg_name_size['file_name']):
                self.load_from_cache(pkg_name_size['file_name'], pkg_name_size['file_size'])
                manager.update_installed_package(pkg_name_size['file_name'], _params=_params)

            else:
                self.__download(_url, pkg_name_size)
                manager.update_installed_package(pkg_name_size['file_name'], _params=_params)

        if _params['type'] == 'install':
            older_version = manager.is_exist_in_any_version(pkg_name_size['file_name'])
            if manager.is_package_registered(pkg_name_size['file_name']):
                name, version = manager.package_split(pkg_name_size['file_name'])
                print Fore.GREEN + "%s (%s)" % (name, version) + Fore.RESET + " is already installed"

            elif older_version is not None:
                name, version = manager.package_split(pkg_name_size['file_name'])
                print "trying to install " + Fore.YELLOW + "%s (%s)" % (name, version) + Fore.RESET
                print Fore.GREEN + "\t%s" % (older_version['name']) + Fore.RESET + " is already installed in version " + Fore.GREEN + "(%s)" % (older_version['version']) + Fore.RESET

            elif manager.is_in_cache(pkg_name_size['file_name']):
                self.load_from_cache(pkg_name_size['file_name'], pkg_name_size['file_size'])
                manager.register_installed_package(pkg_name_size['file_name'], _repository)
            else:
                self.__download(_url, pkg_name_size)
                manager.register_installed_package(pkg_name_size['file_name'], _repository)

        elif _params['type'] == 'download':
            if manager.is_in_cache(pkg_name_size['file_name']):
                self.load_from_cache(pkg_name_size['file_name'], pkg_name_size['file_size'], _params)
            else:
                self.__download(_url, pkg_name_size, _params)

    def startQueue(self, _url_s, _repositories=None, _params=None):
        try:
            if isinstance(_url_s, types.ListType):
                #print 'list'
                length = len(_url_s)
                for index in range(length):
                    self.__get_file(_url_s[index], _repositories[index], _params)

            elif isinstance(_url_s, types.StringType):
                #print 'str'
                self.__get_file(_url_s, _params=_params)

            else:
                raise idm_exception('start queue exception')
        except idm_exception as e:
            print e.value

    def plugInBrowserWithDownloadManager(self, _browser):
        self.__browser = _browser
