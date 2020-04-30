import os
import importlib
import logging
from scape.core.dispatch import DispatchPool
from scape.core.slot import ParserPool
from scape.core.slot import Slot
from .base import BaseCommand


class RunCommand(BaseCommand):
    def execute(self, args):
        self.run()

    @staticmethod
    def run():
        logger = logging.getLogger("scape")
        logger.info('Initialize...')
        settings = importlib.import_module(os.environ.get('SCAPE_SETTINGS'))
        slot = Slot(settings.SENSORS)
        ParserPool(settings.PARSERS)
        DispatchPool(settings.EXECUTORS, settings.POOL_SIZE)
        slot.start()
