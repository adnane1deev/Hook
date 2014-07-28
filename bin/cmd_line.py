__author__ = 'Adnane deev'

import re
import argparse
import cli_browser
import helper_functions as d
import hook_system_variables as hook
from colorama import init, Fore, Back
from HTMLParser import HTMLParser
from datetime import datetime
import os_operations as op


class cmd_line(object):

    def __init__(self):
        self.__parser = argparse.ArgumentParser(
            prog=hook.application_name,
            description=Fore.GREEN+hook.application_description+Fore.RESET,
            epilog=Back.BLUE+hook.additional_description+Back.RESET,
            usage=hook.usage_syntax,
            version=Fore.YELLOW+hook.application_name+hook.application_version+Fore.RESET,
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

    def __cmd_create(self):
        print

    def __cmd_install(self):
        print

    def __cmd_search(self):
        print

    def __cmd_list(self):
        print

    def __cmd_update(self):
        print

    def __cmd_uninstall(self):
        print

    def __cmd_profile(self):
        print

    def __cmd_home(self):
        print

    def __cmd_cache(self):
        print

    def __initCommands(self):
        self.__parser.add_argument('commands', nargs="*")
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
        self.__parser.add_argument("-s", "--surf", help="Tells if you want to get specific version of packages", action="store_true")

    def __setup_workspace(self, _packages, _settings):
        op.create_directory('.hook')
        op.create_file('.hook/workspace_settings.json', op.object_to_json(_settings))
        op.hide_directory('.hook')
        op.generate_json_file("hook.json", _packages)
        print "Initialized empty HooK workspace in {0}".format(op.get_current_path())
        print "Generating hook.json ..."

    def __parseArguments(self):
        return self.__parser.parse_args()

    def initializeCommandLineTool(self):
        self.__initCommands()
        self.__initOptions()
        return self.__parseArguments()

    def logoPrint(self):
        init()
        print hook.application_logo

    def execute(self, args):
        try:
            commands = args.commands
            if commands[0] == 'init':
                self.__cmd_init(args.interactive, args.pversion, commands)

            elif commands[0] == 'create':
                print 'create =>'
            elif commands[0] == 'install':
                print 'install =>'
            elif commands[0] == 'search':
                print 'search =>'
            elif commands[0] == 'list':
                print 'list =>'
            elif commands[0] == 'update':
                print 'update =>'
            elif commands[0] == 'uninstall':
                print 'uninstall =>'
            elif commands[0] == 'profile':
                print 'profile =>'
            elif commands[0] == 'home':
                print 'home =>'
            elif commands[0] == 'cache':
                print 'cache =>'
            else:
                self.__parser.print_help()

        except IndexError as ex:
            print Back.RED, 'No command was specified (-_-)', Back.RESET, "\n"
            self.__parser.print_help()

"""
cmmd = cmd_line()
cmmd.logoPrint()
args = cmmd.initializeCommandLineTool()
cmmd.execute(args)
"""