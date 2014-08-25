#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
import json
import re


def pretty_print(_list):
    s = pprint.PrettyPrinter()
    s.pprint(object=_list)


def load_json_file(__FilePath=None):
    try:
        __file = open(__FilePath, 'r')
        data = __file.read()
        __file.close()
        return json.loads(data)
    except ValueError:
        return ""


def object_to_json(_json_object):
    return json.dumps(_json_object, indent=4)


def prettify(__json, __indent=4):
    print json.dumps(__json, indent=__indent)


def is_ssh_url(_ssh):
    if re.match(r"^[a-zA-Z0-9._]+\@[a-zA-Z0-9._]+\.[a-zA-Z]{3,}:[\w\-]+/[\w\-\.]+\.git$", _ssh) is not None:
        return True

    return False


def is_http_url(_http):
    if re.match(r"https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?", _http) is not None:
        return True

    return False


def is_repository(_repository):
    if re.match(r"[\w\-]+/[\w\-\.]+", _repository, re.IGNORECASE) is not None:
        return True

    return False
