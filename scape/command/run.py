import os
import importlib
import logging
import logging.config
from scape.conf.settings import DEFAULT_LOGGING
from scape.framework.receive import Receiver
from scape.framework.dispatch import Dispatcher
from scape.framework.recognize import Recognizer
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
        logger.info('Receiver Initialize...')
        receiver = Receiver(settings.SENSORS)
        logger.info('Receiver Ready')
        logger.info('Dispatcher Initialize...')
        Dispatcher(settings.EXECUTORS, settings.POOL_SIZE)
        logger.info('Dispatcher Ready')
        logger.info('Recognizer Initialize...')
        Recognizer(settings.PARSERS)
        logger.info('Recognizer Ready')
        receiver.start()
