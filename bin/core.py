__author__ = 'Asus'

import json


class core_decoder(object):

    @staticmethod
    def loadJsonFile(__FilePath=None):
        __file = open("../hook.json", 'r')
        data = __file.read()
        __file.close()
        decodeddata = json.loads(data)
        print decodeddata['configs']['pagination']