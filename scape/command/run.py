import os
import importlib
from scape.core.dispatch import DispatchPool
from scape.core.parser import ParserPool
from scape.core.slot import Slot


def run(args):
    settings = importlib.import_module(os.environ.get('SCAPE_SETTINGS'))
    DispatchPool(settings.EXECUTORS, settings.POOL_SIZE)
    ParserPool(settings.PARSERS)
    slot = Slot(settings.SENSORS)
    slot.start()


