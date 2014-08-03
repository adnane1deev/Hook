#!/usr/bin/python
# -*- coding: utf-8 -*-

from colorama import Fore

application_logo = Fore.GREEN+'''

                                                `@@@@@@@@ `
                                               ` @@@@@@@,`
                                                 @@@@@@@`
                                                ` @@@@@@  `
                                               `   @@@+  `
      _/    _/                      _/    _/      ` @@  `
     _/    _/    _/_/      _/_/    _/  _/        `  `+@:
    _/_/_/_/  _/    _/  _/    _/  _/_/          `  `  `@` `
   _/    _/  _/    _/  _/    _/  _/  _/        ` :`  ` @@`
  _/    _/    _/_/      _/_/    _/    _/         `@ `  @@
                                                ` @@   @` `
                                               `  `#@@@' `

'''+Fore.RESET

application_name = 'Hook'
application_description = 'Hook for the entire web workflow'
additional_description = ' Working on new features coming out soon '
usage_syntax = '%(prog)s <command> [<args>] [<options>]'
application_version = '(1.0.0 Alpha)'
data_storage_path = 'Hook/cache'