#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging


class debugger_(object):

    def __init__(self, logger_name='Hook logger'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        self.file_handler = logging.FileHandler(filename="test.log", encoding='utf-8')
        self.file_handler.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter('%(asctime)s - %(filename)s/Line: %(lineno)d - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def setFormatterStringAndDateFMT(self, formatter_string, date_fmt):
        self.formatter = logging.Formatter(formatter_string, datefmt=date_fmt)
        self.file_handler.setFormatter(self.formatter)

    def printLog(self, _message, _type='log'):
        if _type == 'log':
            self.__log(_message)
        elif _type == 'debug':
            self.__debug(_message)
        elif _type == 'info':
            self.__info(_message)
        elif _type == 'error':
            self.__error(_message)
        elif _type == 'warning':
            self.__warning(_message)
        elif _type == 'exception':
            self.__exception(_message)
        else:
            self.__log(_message)

    def __log(self, _message):
        """
        Level 	    Numeric value
        =========================
        CRITICAL    50
        ERROR       40
        WARNING     30
        INFO        20
        DEBUG       10
        NOTSET      0
        """
        self.logger.log(50, _message)

    def __debug(self, _message):
        self.logger.debug(_message)

    def __info(self, _message):
        self.logger.info(_message)

    def __error(self, _message):
        self.logger.error(_message)

    def __warning(self, _message):
        self.logger.warning(_message)

    def __exception(self, _message):
        self.logger.exception(_message)


debugger = debugger_()
debugger.printLog(_message="Note that you may use INTEGER var instead of FLOAT", _type="warning")
