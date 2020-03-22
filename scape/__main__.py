import sys
import scape
from scape.command import *


def run_with_command():
    if len(sys.argv) > 1 and callable(locals()[sys.argv[1]]):
        locals()[sys.argv[1]](sys.argv[2:])


if __name__ == '__main__':
    run_with_command()
