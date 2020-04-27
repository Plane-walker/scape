import sys
from .init import InitCommand
from .run import RunCommand


COMMAND = {'init': InitCommand(), 'run': RunCommand()}


def run_with_command():
    args = sys.argv[1:]
    if len(args) > 0 and args[0] in COMMAND.keys():
        COMMAND[args[0]].execute(args[1:])
