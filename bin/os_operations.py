__author__ = 'Asus'
# http://stackoverflow.com/questions/19622133/python-set-hide-attribute-on-folders-in-windows-os

import os
import sys
import re
import ctypes
import distutils.dir_util as dir_util
from os.path import expanduser


def define_operation_system():
    platform_name = sys.platform
    if re.search(r'win', platform_name, re.IGNORECASE):
        return 'windows'

    elif re.search(r'linux', platform_name, re.IGNORECASE):
        return 'linux'


def remove_file(_path):
    if os.path.exists(_path):
        os.unlink(_path)


def remove_directory(_path):
    #distutils.dir_util.remove_tree(directory[, verbose=0, dry_run=0])
    if os.path.exists(_path):
        try:
            os.rmdir(_path)
        except OSError as we:
            dir_util.remove_tree(_path)


def create_file(_file_name, _content=''):
    if not os.path.exists(_file_name):
        with open(_file_name, "w") as handler:
            handler.write(_content)


def create_directory(_dir_name):
    if not os.path.exists(_dir_name):
        os.mkdir(_dir_name)


def hide_file(_path):
    if __check_environment(_path):
        try:
            __hide(_path)
        except Exception as e:
            print e.message


def hide_directory(_path):
    hide_file(_path)


def __hide(_name):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ret = ctypes.windll.kernel32.SetFileAttributesW(ur''+_name, FILE_ATTRIBUTE_HIDDEN)

    if ret:
        print 'attribute set to Hidden'
    else:  # return code of zero indicates failure, raise Windows error
        raise WinError()


def __check_environment(_path):
    if define_operation_system() == 'windows' and os.path.exists(_path):
        return True


def get_home():
    return expanduser("~")


if define_operation_system() == 'windows':
    from ctypes import WinError

"""
    os.path
"""
"""
print os.path.isfile("E:\Formations\exemples")
print os.path.isfile("E:\Formations\exemples\exemple.html")
print os.path.split("E:\Formations\exemples\exemple.html")


print os.name
print sys.platform

print re.search(r'win', 'sdsin32ds', re.IGNORECASE)
if not os.path.exists(".hook"):
    print "eeee"
"""

print get_home()