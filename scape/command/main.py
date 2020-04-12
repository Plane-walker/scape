import sys
from .init import init
from .run import run


def run_with_command():
    args = sys.argv[1:]
    if len(args) > 0 and callable(globals()[args[0]]):
        command = args[0]
        globals()[command](args[1:])
