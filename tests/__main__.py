"""
Command-line interface to aigym.tests.

usage: python -m aigym.tests [-h] [-run]

optional arguments:
  -h, --help  show this help message and exit
  -run        runs aigym tests

"""
import os
from argparse import ArgumentParser
from subprocess import run

from aigym.logging import logger

from aigym import tests

argument_parser = ArgumentParser('aigym.tests')
argument_parser.add_argument('-run', action='store_true', help="runs aigym tests")

parsed_arguments = argument_parser.parse_args()

if parsed_arguments.run:
    logger.debug("testing started...")
    for filename in tests.__all__:
        logger.debug("testing {} package".format(filename))
        run(['python', '-m', 'unittest', os.path.join(os.path.dirname(__file__), "{}.py".format(filename))])
    logger.debug("testing finished.")
