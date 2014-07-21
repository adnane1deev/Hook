__author__ = 'Adnane deev'

import argparse
import hook_system_variables as hook
from colorama import init, Fore, Back


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

    def __cmd_init(self):
        print

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
        self.__parser.add_argument("-f", "--force", help="Makes various commands more forceful", action="store_false")
        self.__parser.add_argument("-j", "--json", help="Output consumable JSON", action="store_false")

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
                print 'init =>'
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


cmmd = cmd_line()
cmmd.logoPrint()
args = cmmd.initializeCommandLineTool()
cmmd.execute(args)
