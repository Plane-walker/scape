import os
import importlib
from scape.core.dispatch import Dispatcher
from scape.core.slot import Slot


def run(args):
    settings = importlib.import_module(os.environ.get('SCAPE_SETTINGS'))
    dispatcher = Dispatcher(settings.EXECUTORS, settings.CENTERS)
    slot = Slot(dispatcher, settings.SENDERS)
    slot.start()


