import sys
from .init import init
from .run import run


def run_with_command():
    sys.argv.pop(0)
    if len(sys.argv) > 0 and callable(globals()[sys.argv[0]]):
        command = sys.argv.pop(0)
        globals()[command](sys.argv)
