#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
import json


def pretty_print(_list):
    s = pprint.PrettyPrinter()
    s.pprint(object=_list)


def load_json_file(__FilePath=None):
    __file = open(__FilePath, 'r')
    data = __file.read()
    __file.close()
    return json.loads(data)


def prettify(__json, __indent=4):
    print json.dumps(__json, indent=__indent)