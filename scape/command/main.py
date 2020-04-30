import sys
from .init import InitCommand
from .run import RunCommand
import logging.config
from scape.conf.settings import DEFAULT_LOGGING


COMMAND = {'init': InitCommand(), 'run': RunCommand()}


def run_with_command():
    logging.config.dictConfig(DEFAULT_LOGGING)
    args = sys.argv[1:]
    if len(args) > 0 and args[0] in COMMAND.keys():
        COMMAND[args[0]].execute(args[1:])
