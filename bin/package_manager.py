#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from colorama import Fore
import helper_functions as helper
import os_operations as op
import hook_system_variables as hook
import re


def settings_not_found_error_print():
    print "  workspace_settings.json file not found, and this might be of the following reasons :\n"
    print "\t- You not in the workspace directory"
    print "\t- Your workspace haven't been setup yet"
    print "\t- Deleted by accident"


def register_installed_package(_pkg):
    if not op.is_exits('.hook/workspace_settings.json'):
        settings_not_found_error_print()

        return

    created_time = datetime.today().strftime('%H:%M:%S - %b, %d %Y')
    installed_package = {"package": _pkg, "installed_at": created_time}

    settings = helper.load_json_file('.hook/workspace_settings.json')
    settings['installed_packages'].append(installed_package)

    op.create_file('.hook/workspace_settings.json', op.object_to_json(settings))


def is_package_registered(_pkg):
    settings = helper.load_json_file('.hook/workspace_settings.json')
    installed = settings['installed_packages']

    for pkg in installed:
        if pkg['package'] == _pkg:
            return True

    return False


def is_in_cache(_pkg):
    cache_path = op.get_home()+'/'+hook.data_storage_path+'/'+_pkg
    if op.is_exits(cache_path):
        return True

    return False


def match_package(_pkg):
    if not op.is_exits('.hook/workspace_settings.json'):
        settings_not_found_error_print()

        return

    matches = []
    installed_packages = get_installed_packages()
    for item in installed_packages:
        if re.match(r'.*' + _pkg + '.*', item['package'], re.IGNORECASE) is not None:
            matches.append(item)

    return matches


def uninstall_package(_pkg_name, _pkg_version):
    if not op.is_exits("components") or not op.is_exits('.hook/workspace_settings.json'):
        settings_not_found_error_print()
        return

    list_dir = op.list_dir("components")
    settings = helper.load_json_file('.hook/workspace_settings.json')
    installed = settings['installed_packages']

    for item in installed:
        if item['package'] == _pkg_name + '-' + _pkg_version + '.zip':
            installed.remove(item)
            settings['installed_packages'] = installed
            break

    if _pkg_name + '-' + _pkg_version not in set(list_dir):
        print "\n" + _pkg_name + '-' + _pkg_version + 'does not match any folder in components directory'
        return

    op.remove_directory("components/" + _pkg_name + '-' + _pkg_version)
    op.create_file('.hook/workspace_settings.json', op.object_to_json(settings))


def get_installed_packages():
    settings = helper.load_json_file('.hook/workspace_settings.json')
    return settings['installed_packages']


def get_list_of_installed_packages():
    if not op.is_exits('.hook/workspace_settings.json'):
        settings_not_found_error_print()

        return

    installed = get_installed_packages()

    try:
        print Fore.BLUE+"{0:28}{1:28}{2:28}".format("Installed at", "Name", "Version")+Fore.RESET
        print

        for pkg in installed:
            installed_at = pkg['installed_at']
            name, version = re.search(r'(.+?)\-([\d\w\.]*)\.zip', pkg['package'], re.IGNORECASE).groups()

            print "{0:28}{1:28}{2:28}".format(installed_at, name, version)

    except AttributeError as e:
        print e.message

