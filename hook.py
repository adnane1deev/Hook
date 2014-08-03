#!/usr/bin/python
# -*- coding: utf-8 -*-

import bin.cmd_line as command_line


def main():
    command_line_object = command_line.cmd_line()
    command_line_arguments = command_line_object.initializeCommandLineTool()
    command_line_object.execute(command_line_arguments)

if __name__ == '__main__':
    main()