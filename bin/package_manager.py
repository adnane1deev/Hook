
from datetime import datetime
import helper_functions as helper
import os_operations as op
import hook_system_variables as hook


def register_installed_package(_pkg):
    if not op.is_exits('.hook/workspace_settings.json'):
        print "workspace_settings.json file not found, and this might be of the following reasons :"
        print "\t-You not in the workspace directory"
        print "\t-Your workspace haven't been setup yet"
        print "\t-Deleted by accident"

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