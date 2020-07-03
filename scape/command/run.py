import os
import importlib
import logging
import logging.config
from scape.conf.settings import DEFAULT_LOGGING
from scape.core.dispatch import DispatchPool
from scape.core.slot import ParserPool
from scape.core.slot import Slot
from .base import BaseCommand


class RunCommand(BaseCommand):
    def execute(self, args):
        self.run()

    @staticmethod
    def run():
        logging.config.dictConfig(DEFAULT_LOGGING)
        logger = logging.getLogger("scape")
        logger.info('Initialize...')
        settings = importlib.import_module(os.environ.get('SCAPE_SETTINGS'))
        logger.info('Slot Initialize...')
        slot = Slot(settings.SENSORS)
        logger.info('Slot Ready')
        logger.info('DispatchPool Initialize...')
        DispatchPool(settings.EXECUTORS, settings.POOL_SIZE)
        logger.info('DispatchPool Ready')
        logger.info('ParserPool Initialize...')
        ParserPool(settings.PARSERS)
        logger.info('ParserPool Ready')
        slot.start()
