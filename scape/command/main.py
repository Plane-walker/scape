import sys
from .init import init
from .run import run


COMMAND = {'init': init, 'run': run}


def run_with_command():
    args = sys.argv[1:]
    if len(args) > 0 and args[0] in COMMAND.keys():
        COMMAND[args[0]](args[1:])
