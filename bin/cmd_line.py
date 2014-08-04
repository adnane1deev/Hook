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
                            _input = raw_input("Choose your package number (DEFAULT: 1, 0: to ignore): ")
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
                            package_version = raw_input("Choose your package number (DEFAULT: latest): ")
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

            #version = 'master' if pkg['version'] == '*' else pkg['version']


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
            response = cmd_browser.submit()
            repos_list = cmd_browser.parseResponse(response)

            parser = HTMLParser()
            length = len(repos_list)
            for repo_index in range(length):
                tpl = repos_list[repo_index]
                print parser.unescape("[{0:2}] : {1} {2}".format((repo_index+1), tpl[0][1:], '- '+re.sub(r'<em>|</em>', '', tpl[2]).strip()))

            if length > 0:
                if _surfing:
                    print
                    current = cmd_browser.getCurrentPage()
                    print "Current page: {0}".format(current)
                    print "Available pages: ",
                    pages = cmd_browser.parsePagination(response)

                    if av_pages == -1:
                        av_pages = int(pages[-1])

                    if pages is not None:
                        #for page in pages[:]:
                        #    print("{0:1}".format(page)),
                        print av_pages,
                    else:
                        print None
                    prompt_message = "Choose your (package number/action) (1: DEFAULT, p: PREVIOUS, n: NEXT, r: RESET, q: QUIT): "

                print
                package_number = -1
                _input = ''
                try:
                    print
                    _input = raw_input(prompt_message)
                    package_number = int(_input)
                except ValueError:
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
                if len(versions) > 0:
                    print "\n" + Back.BLUE + package_name + Back.RESET + " versions" + "\n"
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

    def __cmd_uninstall(self):
        print

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



    def __cmd_home(self):
        print

    def __cmd_cache(self):
        print

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
                print 'uninstall =>'
            elif commands[0] == 'profile':
                self.__cmd_profile()

            elif commands[0] == 'home':
                print 'home =>'
            elif commands[0] == 'cache':
                print 'cache =>'
            else:
                self.__parser.print_help()

        except IndexError as ex:
            print "\n" + Back.RED, 'Not enough arguments', Back.RESET, ""
            self.__parser.print_help()
