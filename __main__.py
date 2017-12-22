"""
Command-line interface to aigym.

usage: aigym [-h] [-setup] [-check] [-test] [-show what] [-shell]

optional arguments:
  -h, --help  show this help message and exit
  -setup      runs aigym setup
  -check      checks aigym
  -test       runs aigym tests
  -show what  shows requested on console
  -shell      runs aigym python interactive console

"""
import os
from argparse import ArgumentParser
from code import InteractiveConsole

from aigym.logging import logger
from aigym.conf import settings
from aigym.conf.routines import get_dirs_constants_values_from, extract_constants_from, print_constants_from

arg_parser = ArgumentParser('aigym')
arg_parser.add_argument('-setup', action='store_true', help="runs aigym setup")
arg_parser.add_argument('-check', action='store_true', help="checks aigym")
arg_parser.add_argument('-show', metavar='what', help="shows requested on console")
arg_parser.add_argument('-shell', action='store_true', help="runs aigym python interactive console")

parsed_arguments = arg_parser.parse_args()

aigym_settings = extract_constants_from(settings)

emgym_dir_structure = get_dirs_constants_values_from(aigym_settings)
emgym_dir_structure.remove(settings.AIGYM_DIR)

if parsed_arguments.setup:
    for path in emgym_dir_structure:
        if not os.path.exists(path):
            os.mkdir(path)

if parsed_arguments.check:
    valid = True
    for path in emgym_dir_structure:
        if not os.path.exists(path):
            logger.warning("{} doesn't exist".format(path))
            valid = False
            break
    if valid:
        logger.debug("aigym directory structure is ok.")

if parsed_arguments.show:
    if parsed_arguments.show == 'settings':
        print_constants_from(aigym_settings)
    elif parsed_arguments.show == 'log':
        with open(os.path.join(settings.AIGYM_DIR, settings.AIGYM_LOGFILE_FILENAME)) as log_file:
            for log_line in log_file:
                print(log_line)
    else:
        print('Nothing to show for provided name.')

if parsed_arguments.shell:
    from aigym.dataset import Fer2013RawDataset
    interactive_console = InteractiveConsole(locals())
    interactive_console.interact('<aigym shell>')
