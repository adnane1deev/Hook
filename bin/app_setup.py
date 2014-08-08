#!/usr/bin/python
# -*- coding: utf-8 -*-

import hook_system_variables as hook
import os_operations as op
import os


def setup():
    home_dir = op.get_home()
    app_tree = home_dir + op.separator() + hook.data_storage_path

    if not os.path.exists(app_tree):
        op.create_tree(app_tree)
        file_absolute_path = os.path.abspath(__file__)
        base_dir = os.path.split(file_absolute_path)[0]
        hook_absolute_path = base_dir.rsplit(op.separator(), 1)[0]
        append_hook_to_sys_path(hook_absolute_path)
    else:
        print hook.application_name + " is already setup"


def append_hook_to_sys_path(_path):
    os.environ['PATH'] += os.pathsep + _path