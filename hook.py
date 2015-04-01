#!/usr/bin/python
# -*- coding: utf-8 -*-

import bin.cmd_line as command_line
import sys


def main():
    reload(sys)
    sys.setdefaultencoding("utf-8")
    print """
    Up coming features:
    \tcache/repackage
    \tcreate"""
    command_line_object = command_line.cmd_line()
    command_line_arguments = command_line_object.initializeCommandLineTool()
    try:
        command_line_object.execute(command_line_arguments)
    except KeyboardInterrupt:
        print "\n\nGood Bye (^_^)"

if __name__ == '__main__':
    main()