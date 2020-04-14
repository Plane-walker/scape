import os
import importlib
from scape.core.dispatch import DispatchPool
from scape.core.slot import ParserPool
from scape.core.slot import Slot


def run(args):
    settings = importlib.import_module(os.environ.get('SCAPE_SETTINGS'))
    slot = Slot(settings.SENSORS, settings.INIT_ACTIVATE_SIGNALS)
    ParserPool(settings.PARSERS)
    DispatchPool(settings.EXECUTORS, settings.POOL_SIZE)
    slot.start()


