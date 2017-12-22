"""
This module defines command-line interface to aigym.app package.

usage: python -m aigym.app [-h] [-start name] [-check name] [-test name]

optional arguments:
  -h, --help   show this help message and exit.
  -start name  starts a new app with a name 'name' by using default app's structure template.
  -check name  checks app's structure with a name 'name' in a current directory.
  -test name   run tests for an app with a name 'name'.

All commands uses current working directory as a base.
"""
import os
from argparse import ArgumentParser
from subprocess import run

from aigym.logging import logger
from aigym.app.structure import ApplicationStructureTemplate

arg_parser = ArgumentParser('aigym app')
arg_parser.add_argument('-start', metavar='name', help="starts a new app in a current directory with a name 'name'")
arg_parser.add_argument('-check', metavar='name', help="checks an app with a name 'name' in a current directory")
arg_parser.add_argument('-test', metavar='name', help="run tests for an app with a name 'name'")

parsed_arguments = arg_parser.parse_args()

app_struct_template = ApplicationStructureTemplate()

cwd = os.getcwd()

if parsed_arguments.start:
    app_name = parsed_arguments.start
    app_dir_path = os.path.join(cwd, app_name)
    if os.path.exists(app_dir_path):
        logger.warning('{} app cannot be created, because directory {} already exists!'.format(app_name, app_name))
    else:
        os.mkdir(app_dir_path)
        for filename in app_struct_template:
            with open(os.path.join(app_dir_path, filename), 'w+') as app_file:
                app_file.write('\n'.join(app_struct_template[filename]))
        logger.debug('{} app created successfully.'.format(app_name))

if parsed_arguments.check:
    app_name = parsed_arguments.check
    app_dir_path = os.path.join(cwd, app_name)
    if os.path.exists(app_dir_path):
        valid = True
        for filename in app_struct_template:
            if not os.path.exists(os.path.join(app_dir_path, filename)):
                logger.warning('{} app structure is invalid!'.format(app_name))
                valid = False
                break
        if valid:
            logger.debug('{} app structure is ok.'.format(app_name))
    else:
        logger.warning("{} app doesn't exist in {}".format(app_name, cwd))

if parsed_arguments.test:
    app_name = parsed_arguments.test
    app_dir_path = os.path.join(cwd, parsed_arguments.test)
    if os.path.exists(app_dir_path):
        run(['python', '-m', 'unittest', os.path.join(app_dir_path, app_struct_template.tests_filename)])
    else:
        logger.warning("{} app doesn't exist in {}".format(app_name, cwd))
