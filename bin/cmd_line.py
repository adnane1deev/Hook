#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import argparse
import cli_browser
import helper_functions as helpers
import hook_system_variables as hook
from colorama import init, Fore, Back
from HTMLParser import HTMLParser
from datetime import datetime
import os_operations as op
import cli_download_manager as idm
import package_manager as manager
import os
import helper_functions as helper
import app_setup as app
import time


class cmd_line(object):

    def __init__(self):
        self.__parser = argparse.ArgumentParser(
            prog=hook.application_name,
            description=Fore.GREEN + hook.application_description + Fore.RESET,
            epilog=Back.BLUE + hook.additional_description + Back.RESET,
            usage=hook.usage_syntax,
            version=Fore.YELLOW + hook.application_name + ' ' + hook.application_version + Fore.RESET,
            conflict_handler='resolve'
        )

    def __cmd_init(self, _interactive=False, _pversion=False, _commands=None):
        created_time = datetime.today().strftime('%H:%M:%S - %b, %d %Y')
        print '[+] : Created at {0}'.format(created_time)
        print '[+] : Installed packages {0}'.format(0)
        print '[+] : Updates at the working directory {0}'.format(0)
        packages = []

        if _interactive:

            print
            want_more = 'Y'
            while want_more in ('y', 'Y'):
                repository = raw_input("Offer your package name: ")

                if repository in ('q', 'quit', 'exit'):
                    break

                print
                cmd_browser = cli_browser.cli_browser()
                cmd_browser.setRequestedURL("https://github.com/search?q={0}&type=Repositories&ref=searchresults".format(repository))
                response = cmd_browser.submit()
                repos_list = cmd_browser.parseResponse(response)

                parser = HTMLParser()
                length = len(repos_list)
                for repo_index in range(length):
                    tpl = repos_list[repo_index]
                    print parser.unescape("[{0:2}] : {1} {2}".format((repo_index+1), tpl[0][1:], '- '+re.sub(r'<em>|</em>', '', tpl[2]).strip()))

                if length > 0:
                    print
                    package_number = -1
                    while package_number < 0 or package_number > length:
                        try:
                            _input = raw_input("Choose your package number (1: DEFAULT, 0: IGNORE): ")
                            package_number = int(_input)
                        except ValueError:
                            package_number = 1

                    if package_number == 0:
                        continue

                    package_name = repos_list[(package_number-1)][0][1:]
                    package_version = '*'

                    if _pversion:
                        cmd_browser.setRequestedURL('https://github.com/{0}/tags'.format(package_name))
                        response = cmd_browser.submit()
                        versions = cmd_browser.parseVersions(response)
                        if len(versions) > 0:
                            for vr in versions:
                                print vr, ', ',

                            print
                            package_version = raw_input("Choose your package number (latest: DEFAULT): ")
                            if package_version == '':
                                package_version = versions[0]
                        else:
                            print Back.RED+"There is no releases"+Back.RESET

                    po = {"package": package_name, "version": package_version}
                    packages.append(po)

                    print
                    print "[+] : {0} added to your target packages".format(package_name)
                    print
                else:
                    print "There is no package named: {0}".format(repository)

                want_more = raw_input("Do you want more packages (y/N): ")

                cmd_browser.closeConnections()

        else:
            _packages = _commands[1:]
            for pkg in _packages:
                dtls = pkg.split(':')
                packages.append({"package": dtls[0], "version": dtls[1]})

        print
        #d.pretty_print(packages)
        self.__setup_workspace(packages, {"created_at": created_time, "installed_packages": [], "workspace_updates": []})

    def __cmd_self_install(self):
        app.setup()

    def __cmd_create(self):
        print

    def __cmd_install(self):
        browser_object = cli_browser.cli_browser()
        browser_connection = browser_object.getHttpConnection()
        download_manager = idm.download_manager()
        download_manager.plugInBrowserWithDownloadManager(browser_connection)

        list = helpers.load_json_file('hook.json')['require']
        #helpers.prettify(list)

        urls = []

        for pkg in list:
            name = pkg['package']
            version = ''

            if pkg['version'] == '*':
                browser_object.setRequestedURL('https://github.com/{0}/tags'.format(name))
                response = browser_object.submit()
                versions_list = browser_object.parseVersions(response)

                if len(versions_list) == 0:
                    print Back.RED+'No releases for {0}'.format(name)+Back.RESET
                    version = 'master'

                else:
                    version = versions_list[0]

            else:
                version = pkg['version']

            #url = 'https://github.com/fabpot/Twig/archive/v1.16.0.zip'
            url = 'https://github.com/{0}/archive/{1}.zip'.format(name, version)
            #print url
            urls.append(url)

        download_manager.startQueue(urls)

        browser_connection.close()
        browser_object.closeConnections()

    def __cmd_search(self, _package, _surfing=False, _current="1", _av_pages=-1):
        if len(_package) == 0:
            print "No package is provided"
            return

        cmd_browser = cli_browser.cli_browser()

        while True:
            current = _current
            av_pages = _av_pages
            prompt_message = "Choose your package number (1: DEFAULT): "
            repository = _package[0]
            cmd_browser.setRequestedURL("https://github.com/search?q={0}&p={1}&type=Repositories&ref=searchresults".format(repository, current))
            response = ''
            new_line = ''
            while True:
                response = cmd_browser.submit()

                if response is not None:
                    if new_line == "#":
                        print "\n"

                    break
                new_line = "#"
                #cmd_browser.closeConnections()
                #cmd_browser = cli_browser.cli_browser()

                #cmd_browser.setRequestedURL("https://github.com/search?q={0}&p={1}&type=Repositories&ref=searchresults".format(repository, current))
            repos_list = cmd_browser.parseResponse(response)


            parser = HTMLParser()
            length = len(repos_list)
            for repo_index in range(length):
                tpl = repos_list[repo_index]
                print parser.unescape("[{0:2}] : {1} {2}".format((repo_index+1), tpl[0][1:], '- '+re.sub(r'<em>|</em>', '', tpl[2]).strip()))

            if length > 0:
                if _surfing:
                    print
                    current = cmd_browser.getCurrentPage(response)
                    print "Current page: {0}".format(current)
                    print "Available pages: ",
                    pages = cmd_browser.parsePagination(response)

                    if av_pages == -1 and pages is not None:
                        #print pages[-1]
                        #print pages
                        av_pages = int(pages[-1])
                    #if pages is not None:
                        print av_pages,
                    else:
                        if av_pages == -1:
                            av_pages = 1
                        print av_pages if av_pages != -1 else 1

                    prompt_message = "Choose your (package number/action) (1: DEFAULT, p: PREVIOUS, n: NEXT, r: RESET, q: QUIT): "

                print
                package_number = -1
                _input = ''
                try:
                    print
                    _input = raw_input(prompt_message)
                    package_number = int(_input)
                except ValueError:
                    #print av_pages
                    if _surfing and _input in ('p', 'n', 'r', 'q') and 0 < int(current) <= av_pages:
                        print
                        if _input == 'p':
                            _current = str(int(current)-1)
                            _av_pages = av_pages
                        elif _input == 'n':
                            crnt = int(current)+1
                            if crnt > av_pages:
                                crnt = av_pages

                            _current = str(crnt)
                            _av_pages = av_pages
                        elif _input == 'r':
                            _current = '1'
                            _av_pages = av_pages

                        else:
                            print "Hook is quitting ..."
                            cmd_browser.closeConnections()
                            return

                        continue

                    elif _input == 'q':
                        print "Hook is quitting ..."
                        cmd_browser.closeConnections()
                        return

                    else:
                        package_number = 1

                if package_number < 0:
                    package_number = 1

                elif package_number > length:
                    package_number = length

                package_name = repos_list[(package_number-1)][0][1:]

                cmd_browser.setRequestedURL('https://github.com/{0}/tags'.format(package_name))
                response = cmd_browser.submit()
                versions = cmd_browser.parseVersions(response)
                print "\n" + Back.BLUE + package_name + Back.RESET + " versions" + "\n"
                if len(versions) > 0:

                    for vr in versions:
                        print vr, ', ',

                else:
                    print Back.RED+"There is no releases"+Back.RESET

            else:
                print "There is no package named: {0}".format(repository)

            break
        cmd_browser.closeConnections()


    def __cmd_list(self):
        manager.get_list_of_installed_packages()

    def __cmd_update(self):
        print

    def __uninstall_helper_interface(self, installed_list):
        length = len(installed_list)
        _input = ''
        try:
            print Fore.BLUE+"{0:4}  {1:28}{2:28}{3:28}".format("Num", "Installed at", "Name", "Version")+Fore.RESET
            print
            for item_index in range(length):
                pkg = installed_list[item_index]
                installed_at = pkg['installed_at']
                name, version = re.search(r'(.+?)\-([\d\w\.]*)\.zip', pkg['package'], re.IGNORECASE).groups()

                print "[{0:2}]  {1:28}{2:28}{3:28}".format((item_index+1), installed_at, name, version)

            print
            while True:
                _input = raw_input("Choose your package number (1: DEFAULT, q: QUIT): ")
                if _input == "":
                    _input = 1

                package_index = int(_input)

                if 0 < package_index <= length:
                    pkg = installed_list[package_index-1]
                    name, version = re.search(r'(.+?)\-([\d\w\.]*)\.zip', pkg['package'], re.IGNORECASE).groups()
                    print
                    print Back.RED + " DANGER ZONE " + Back.RESET

                    while True:
                        confirmation = raw_input("\n\t" + Fore.RED + "{0} ({1})".format(name, version) + Fore.RESET + " is going to be deleted. Are you sure (y,N): ")

                        if confirmation in ('y', 'Y', 'yes'):
                            manager.uninstall_package(name, version)
                            print "Delete action on "+name
                            break
                        elif confirmation in ('', 'n', 'N', 'no'):
                            print "\nOperation is canceled"
                            print "Hook is quitting"
                            break
                    break

        except ValueError:
            if _input not in ('q', 'quit'):
                print "No value was specified"
            print "Hook is quitting"
        except AttributeError as e:
            print e.message

    def __cmd_uninstall(self, _packages=None):
        if _packages is None or _packages == []:
            installed_list = manager.get_installed_packages()
            if len(installed_list) > 0:
                self.__uninstall_helper_interface(installed_list)

            else:
                print Fore.YELLOW + "No packages were installed yet" + Fore.RESET
            return

        item_to_uninstall = _packages[0]
        matching_list = manager.match_package(item_to_uninstall)
        if len(matching_list) > 0:
            print Back.BLUE + " Package(s) matching " + Back.RESET + " ({0})\n".format(item_to_uninstall)
            self.__uninstall_helper_interface(manager.match_package(item_to_uninstall))

        else:
            print Fore.YELLOW + "No package matches " + Fore.RESET + "({0})\n".format(item_to_uninstall)

    def __cmd_profile(self):
        if not op.is_exits('.hook/workspace_settings.json'):
            manager.settings_not_found_error_print()
            return

        if not op.is_exits("hook.json"):
            print "You're not in the working directory. Switch to the working directory and try again"
            return

        settings = helper.load_json_file('.hook/workspace_settings.json')

        print Back.BLUE + " Workspace: " + Back.RESET + " %0.2f MB\n" % op.get_folder_size(os.getcwd())['mb']
        print "\t" + Fore.BLUE + "Created at:" + Fore.RESET + " {0}\n".format(settings['created_at'])

        print Back.BLUE + " Components: " + Back.RESET + " %0.1f MB\n" % op.get_folder_size('components')['mb']

        components = os.listdir('components')
        print "\t" + Fore.BLUE+"{0:32}{1:14}{2:14}\n".format("Name", "Size/(mb)", "Size/(kb)")+Fore.RESET

        for item in components:
            size = op.get_folder_size('components/' + item)
            print "\t" + "{0:32}{1:14}{2:14}".format(item, ("%0.2f" % size['mb']), ("%d" % size['kb']))

    def __cmd_home(self, _repository):
        url = ''
        if helper.is_ssh_url(_repository):
            url = 'https://github.com/' + re.search(r':(.+?).git$', _repository, re.IGNORECASE).group(1)

        elif helper.is_http_url(_repository):
            url = _repository

        elif helper.is_repository(_repository):
            url = 'https://github.com/' + _repository

        if url == '':
            print "No proper information was given"
            return

        cmd_browser = cli_browser.cli_browser()
        cmd_browser.setRequestedURL(url)
        print Fore.GREEN + 'Requesting' + Fore.RESET + ' -> ' + url
        response = cmd_browser.submit(_return_status_code=True)

        try:
            response_status = int(response)
            print Fore.YELLOW + str(response_status) + Fore.RESET + ': ' + cmd_browser.status_code_desc(response_status)
        except ValueError as e:
            print Fore.GREEN + 'Opening' + Fore.RESET + ' -> ' + url + ' in the default web browser'
            op.open_url(url)

    def __cache_list(self):
        cache_list = op.list_dir(op.get_home() + op.separator() + hook.data_storage_path)
        length = len(cache_list)
        print Fore.BLUE + "{0:4} {1:35}{2:10}".format("Num", "File name", "Type") + Fore.RESET
        print
        for index in range(length):
            try:
                cached_file = cache_list[index]
                name, type = re.search(r'(.+?)\.(zip|rar|gzip|bzip2|tar)', cached_file, re.IGNORECASE).groups()

                print "[{0:2}] {1:35}{2:10}".format((index+1), name, type)
            except Exception:
                pass

    def __cache_remove(self, _args):
        separator = op.separator()
        cache_path = op.get_home() + separator + hook.data_storage_path
        cache_list = op.list_dir(cache_path)
        if len(_args) > 0:
            file_name = _args[0]
            matching_list = manager.match_package_by_list(cache_list, file_name)
            length = len(matching_list)
            if length == 0:
                print Fore.YELLOW + 'No file matches ' + Fore.RESET + "({0})\n".format(file_name)
                return

            if length == 1:
                file_name = matching_list[0]
                print Back.RED + " DANGER ZONE " + Back.RESET
                while True:
                    confirmation = raw_input("\n\t" + Fore.RED + file_name + Fore.RESET + " is going to be deleted. Are you sure (y,N): ")
                    if confirmation in ('y', 'Y', 'yes'):
                        op.remove_file(cache_path + separator + file_name)
                        print "\n" + Fore.YELLOW + file_name + Fore.RESET + " has been deleted"
                        break
                    elif confirmation in ('', 'n', 'N', 'no'):
                        print "\nOperation is canceled"
                        print "Hook is quitting"
                        break
                return

            _input = ''
            try:
                print Back.BLUE + ' File(s) matching ' + Back.RESET + " ({0})".format(file_name)
                print
                print Fore.BLUE + "{0:4} {1:30}".format('Num', 'File name') + Fore.RESET
                print
                for index in range(length):
                    print "[{0:2}] {1:30}".format((index + 1), matching_list[index])

                print
                while True:
                    _input = raw_input("Choose your file number (1: DEFAULT, q: QUIT): ")
                    if _input == "":
                        _input = 1

                    file_index = int(_input)
                    if 0 < file_index <= length:
                        file_name = matching_list[(file_index - 1)]
                        print "\n" + Back.RED + " WARNING " + Back.RESET + " Selected[{0}]".format(Fore.YELLOW + file_name + Fore.RESET)

                        while True:
                            confirmation = raw_input("\n\t" + Fore.RED + file_name + Fore.RESET + " is going to be deleted. Are you sure (y,N): ")
                            if confirmation in ('y', 'Y', 'yes'):
                                op.remove_file(cache_path + separator + file_name)
                                print "\n" + Fore.YELLOW + file_name + Fore.RESET + " has been deleted"
                                break
                            elif confirmation in ('', 'n', 'N', 'no'):
                                print "\nOperation is canceled"
                                print "Hook is quitting"
                                break
                        break
            except ValueError:
                if _input not in ('q', 'quit'):
                    print "No value was specified"
                    print "Hook is quitting"
            except AttributeError as e:
                print e.message

            return

        _input = ''
        try:
            length = len(cache_list)
            print Fore.BLUE + "{0:4} {1:30}".format('Num', 'File name') + Fore.RESET
            print
            for index in range(length):
                print "[{0:2}] {1:30}".format((index + 1), cache_list[index])

            print
            while True:
                _input = raw_input("Choose your file number (1: DEFAULT, q: QUIT): ")
                if _input == "":
                    _input = 1

                file_index = int(_input)
                if 0 < file_index <= length:
                    file_name = cache_list[(file_index - 1)]
                    print "\n" + Back.RED + " WARNING " + Back.RESET + " Selected[{0}]".format(Fore.YELLOW + file_name + Fore.RESET)

                    while True:
                        confirmation = raw_input("\n\t" + Fore.RED + file_name + Fore.RESET + " is going to be deleted. Are you sure (y,N): ")
                        if confirmation in ('y', 'Y', 'yes'):
                            op.remove_file(cache_path + separator + file_name)
                            print "\n" + Fore.YELLOW + file_name + Fore.RESET + " has been deleted"
                            break
                        elif confirmation in ('', 'n', 'N', 'no'):
                            print "\nOperation is canceled"
                            print "Hook is quitting"
                            break
                    break
        except ValueError:
            if _input not in ('q', 'quit'):
                print "No value was specified"
                print "Hook is quitting"
        except AttributeError as e:
            print e.message


    def __cache_info(self):
        separator = op.separator()
        cache_path = op.get_home() + separator + hook.data_storage_path
        cache_list = op.list_dir(cache_path)
        length = len(cache_list)
        print Fore.BLUE + "{0:4} {1:35}{2:8}{3:28}{4:14}{5:14}".format("Num", "File name", "Type", "time", "Size/(mb)", "Size/(kb)") + Fore.RESET
        print
        for index in range(length):
            try:
                cached_file = cache_list[index]
                name, type = re.search(r'(.+?)\.(zip|rar|gzip|bzip2|tar)', cached_file, re.IGNORECASE).groups()
                file_size = op.get_file_size(cache_path + separator + cached_file)
                t = os.path.getmtime(cache_path + separator + cached_file)  # returns seconds
                m = time.strftime("%H:%M:%S - %b, %d %Y", time.gmtime(t))
                print "[{0:2}] {1:35}{2:8}{3:28}{4:14}{5:14}".format((index+1), name, type, m, ("%0.2f" % file_size['mb']), ("%d" % file_size['kb']))
            except Exception:
                pass

    def __cache_rename(self, _args):
        old_name = _args[0]
        new_name = _args[1]

        separator = op.separator()
        cache_path = op.get_home() + separator + hook.data_storage_path
        cache_list = op.list_dir(cache_path)

        matching_list = manager.match_package_by_list(cache_list, old_name)
        length = len(matching_list)
        if length == 0:
            print Fore.YELLOW + 'No file matches ' + Fore.RESET + "({0})\n".format(old_name)
            return

        if length == 1:
            old_name = matching_list[0]
            oldname_file_extension = manager.get_file_extension(old_name)
            newname_file_extension = manager.get_file_extension(new_name)
            extension = manager.choose_extension(oldname_file_extension, newname_file_extension)
            if extension is not None:
                new_name += '.'+extension

            op.rename_file(cache_path + separator + old_name, cache_path + separator + new_name)
            print Fore.YELLOW + old_name + Fore.RESET + ' renamed -> ' + Fore.GREEN + new_name + Fore.RESET
            return

        _input = ''
        try:
            print Back.BLUE + ' File(s) matching ' + Back.RESET + " ({0})".format(old_name)
            print
            print Fore.BLUE + "{0:4} {1:30}".format('Num', 'File name') + Fore.RESET
            print
            for index in range(length):
                print "[{0:2}] {1:30}".format((index + 1), matching_list[index])

            print
            while True:
                _input = raw_input("Choose your file number (1: DEFAULT, q: QUIT): ")
                if _input == "":
                    _input = 1

                file_index = int(_input)
                if 0 < file_index <= length:
                    old_name = matching_list[(file_index - 1)]
                    print "\n" + Back.RED + " WARNING " + Back.RESET + " Selected[{0}]".format(Fore.YELLOW + old_name + Fore.RESET)

                    while True:
                        confirmation = raw_input("\n\tAre you sure (y,N): ")
                        if confirmation in ('y', 'Y', 'yes'):
                            oldname_file_extension = manager.get_file_extension(old_name)
                            newname_file_extension = manager.get_file_extension(new_name)
                            extension = manager.choose_extension(oldname_file_extension, newname_file_extension)
                            if extension is not None:
                                new_name += '.'+extension

                            op.rename_file(cache_path + separator + old_name, cache_path + separator + new_name)
                            print "\n" + Fore.YELLOW + old_name + Fore.RESET + ' renamed -> ' + Fore.GREEN + new_name + Fore.RESET
                            break
                        elif confirmation in ('', 'n', 'N', 'no'):
                            print "\nOperation is canceled"
                            print "Hook is quitting"
                            break
                    break

        except ValueError:
            if _input not in ('q', 'quit'):
                print "No value was specified"
                print "Hook is quitting"
        except AttributeError as e:
            print e.message

    def __cache_help(self):
        print "usage: hook cache <command> [<args>] [<options>]\n"
        print "Commands:"
        print "{0}{1:19}{2}".format((" " * 2), 'help', "show this help message")
        print "{0}{1:19}{2}".format((" " * 2), 'list', "list cached files")
        print "{0}{1:19}{2}".format((" " * 2), 'info', "show basic information about cached files")
        print "{0}{1:19}{2}".format((" " * 2), 'remove', "remove selected file from cache")
        print "{0}{1:19}{2}".format((" " * 2), 'rename', "rename selected cached file")

    def __cmd_cache(self, cache_cmd):
        """
        cache related commands: list, remove, info, rename
        """
        if cache_cmd[0] == 'list':
            self.__cache_list()

        elif cache_cmd[0] == 'remove':
            self.__cache_remove(cache_cmd[1:])

        elif cache_cmd[0] == 'info':
            self.__cache_info()

        elif cache_cmd[0] == 'rename':
            self.__cache_rename(cache_cmd[1:])

        elif cache_cmd[0] == 'help':
            self.__cache_help()

        else:
            print Back.RED + " Unrecognized command " + Back.RESET
            self.__cache_help()

    def __initCommands(self):
        self.__parser.add_argument('commands', nargs="*")
        self.__parser.add_argument('self-install', help="Setup working environment of hook it self", nargs="?")
        self.__parser.add_argument('init', help="Interactively create a hook.json file", nargs="?")
        self.__parser.add_argument('create', help="Setting up environment for the project", nargs="*")
        self.__parser.add_argument("install", help="Install a package(s) locally", nargs="*")
        self.__parser.add_argument("search", help="Search for a package by name", nargs="?")
        self.__parser.add_argument("list", help="List local packages", nargs="?")
        self.__parser.add_argument("update", help="Update a local package", nargs="?")
        self.__parser.add_argument("uninstall", help="Remove a local package", nargs="?")
        self.__parser.add_argument("profile", help="Show memory usage of the working directory", nargs="?")
        self.__parser.add_argument("home", help="Opens a package homepage into your default browser", nargs="?")
        self.__parser.add_argument("cache", help="Manage hook cache", nargs="?")

    def __initOptions(self):
        self.__parser.add_argument("-f", "--force", help="Makes various commands more forceful", action="store_true")
        self.__parser.add_argument("-j", "--json", help="Output consumable JSON", action="store_true")
        self.__parser.add_argument("-i", "--interactive", help="Makes various commands work interactively", action="store_true")
        self.__parser.add_argument("-p", "--pversion", help="Tells if you want to get specific version of packages", action="store_true")
        self.__parser.add_argument("-s", "--surf", help="Allows you to paginate packages list", action="store_true")

    def __setup_workspace(self, _packages, _settings):
        op.create_directory('.hook')
        op.create_file('.hook/workspace_settings.json', op.object_to_json(_settings))
        #op.hide_directory('.hook')
        op.show_directory('.hook')
        op.create_directory('components')
        op.generate_json_file("hook.json", _packages)
        print "Initialized empty HooK workspace in {0}".format(op.get_current_path())
        print "Generating hook.json ..."

    def __is_workspace_setup(self):
        hook_exists = op.is_exits('.hook')
        workspace_settings_exists = op.is_exits('.hook/workspace_settings.json')
        components_exists = op.is_exits('components')
        hook_json = op.is_exits('hook.json')

        if hook_exists and workspace_settings_exists and components_exists and hook_json:
            return True

        return False

    def __parseArguments(self):
        return self.__parser.parse_args()

    def initializeCommandLineTool(self):
        self.__initCommands()
        self.__initOptions()
        return self.__parseArguments()

    def logoPrint(self, _logo=''):
        init()
        if _logo == 'init':
            print hook.application_logo
            return

        print

    def execute(self, args):
        try:
            commands = args.commands
            self.logoPrint(commands[0])
            if commands[0] == 'init':

                if not self.__is_workspace_setup():
                    self.__cmd_init(args.interactive, args.pversion, commands)

                else:
                    print "Workspace already setup"

            elif commands[0] == 'self-install':
                self.__cmd_self_install()

            elif commands[0] == 'create':
                print 'create =>'
            elif commands[0] == 'install':
                self.__cmd_install()

            elif commands[0] == 'search':
                self.__cmd_search(commands[1:], args.surf)

            elif commands[0] == 'list':
                self.__cmd_list()

            elif commands[0] == 'update':
                print 'update =>'
            elif commands[0] == 'uninstall':
                if not self.__is_workspace_setup():
                    manager.settings_not_found_error_print()

                    return
                self.__cmd_uninstall(commands[1:])

            elif commands[0] == 'profile':
                self.__cmd_profile()

            elif commands[0] == 'home':
                self.__cmd_home(commands[1])

            elif commands[0] == 'cache':
                try:
                    self.__cmd_cache(commands[1:])

                except Exception:
                    print Fore.YELLOW + "Not enough arguments" + Fore.RESET
            else:
                self.__parser.print_help()

        except IndexError as ex:
            print "\n" + Back.RED + Fore.WHITE + ' Not enough arguments ' + Fore.RESET + Back.RESET
            self.__parser.print_help()
