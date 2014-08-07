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

    else:
        print hook.application_name + " is already setup"
