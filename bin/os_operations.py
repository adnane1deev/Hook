#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import ctypes
import distutils.dir_util as dir_util
from os.path import expanduser
from zipfile import *
import webbrowser
try:
    from Tkinter import Tk
except ImportError:
    pass


def define_operation_system():
    platform_name = sys.platform
    if re.search(r'win', platform_name, re.IGNORECASE):
        return 'windows'

    elif re.search(r'linux', platform_name, re.IGNORECASE):
        return 'linux'


def list_dir(_dir):
    return os.listdir(_dir)


def rename_file(_old_name, _new_name):
    if is_exits(_old_name):
        os.rename(_old_name, _new_name)
        return True

    return False


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
    """
    if not os.path.exists(_file_name):
        with open(_file_name, "w") as handler:
            handler.write(_content)
    """
    with open(_file_name, "w+") as handler:
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


def show_file(_path):
    if __check_environment(_path):
        try:
            __show(_path)
        except Exception as e:
            print e.message


def hide_directory(_path):
    hide_file(_path)


def show_directory(_path):
    show_file(_path)


def __hide(_name):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ret = ctypes.windll.kernel32.SetFileAttributesW(ur''+_name, FILE_ATTRIBUTE_HIDDEN)

    if ret:
        print #'attribute set to Hidden'
    else:  # return code of zero indicates failure, raise Windows error
        raise WinError()


def __show(_name):
    FILE_ATTRIBUTE_VISIBLE = 0x04
    ret = ctypes.windll.kernel32.SetFileAttributesW(ur''+_name, FILE_ATTRIBUTE_VISIBLE)

    if ret:
        print #'attribute set to visible'
    else:  # return code of zero indicates failure, raise Windows error
        raise WinError()


def __check_environment(_path):
    if define_operation_system() == 'windows' and os.path.exists(_path):
        return True


def get_home():
    return expanduser("~")


def get_current_path():
    return os.path.abspath(".")


def object_to_json(_json_object):
    return json.dumps(_json_object, indent=4)


def generate_json_file(_filename, _pkg_list):
    json_object = {"require": _pkg_list}
    content = object_to_json(json_object)
    create_file(_filename, content)


def separator():
    if define_operation_system() == 'windows':
        return '\\'

    return '/'


def create_tree(_tree):
    os.makedirs(_tree)


def is_exits(_path):
    return os.path.exists(_path)


def decompress_zipfile(_filename, _to_path):
    try:
        zip_archive = ZipFile(_filename, mode="r", compression=ZIP_STORED, allowZip64=False)
        zip_archive.extractall(path=_to_path)
        zip_archive.close()
    except IOError as (nerror, strerror):
        print nerror, ' ', strerror
    except BadZipfile as e:
        print e.message


def get_folder_size(_path="."):
    if not is_exits(_path):
        return

    folder = _path
    folder_size = 0

    for (path, dirs, files) in os.walk(folder):
        for _file in files:
            filename = os.path.join(path, _file)
            folder_size += os.path.getsize(filename)

    return {'mb': to_mb(folder_size), 'kb': to_kb(folder_size)}


def to_mb(_bits):
    return _bits/(1024*1024.0)


def to_kb(_bits):
    return _bits/1024.0


def get_file_size(_path):
    if not is_exits(_path):
        return

    file_size = os.path.getsize(_path)
    return {'mb': (file_size/(1024*1024.0)), 'kb': (file_size/1024.0)}


def open_url(_url):
    """
    Opens URL in DEFAULT browser
    :param _url:
    :return:
    """
    webbrowser.open(_url)


def copy_to_clipboard(_str):
    tk = Tk()
    tk.withdraw()
    tk.clipboard_clear()
    tk.clipboard_append(_str)
    tk.destroy()


if define_operation_system() == 'windows':
    from ctypes import WinError
