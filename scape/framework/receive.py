import importlib
import logging
import signal as listener
from scape.framework.recognize import Recognizer
from scape.framework.dispatch import Dispatcher


class Receiver:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, sensors):
        self.sensors = {}
        self.activate_signal = []
        for sensor in sensors:
            module, sensor = sensor.rsplit('.', 1)
            module = importlib.import_module(module)
            sensor = getattr(module, sensor)()
            self.sensors[sensor.__class__.__name__] = sensor

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def init_signal_status(self, signal):
        sensor = signal.get_processor_name()
        if sensor not in self.sensors.keys():
            raise
        self.sensors[sensor].init_signal_status(signal)

    def update_signal_status(self, signal):
        sensor = signal.get_processor_name()
        if sensor not in self.sensors.keys():
            raise
        self.sensors[sensor].update_signal_status(signal)

    def activate(self, signal):
        if signal not in self.activate_signal:
            self.activate_signal.append(signal)
            self.init_signal_status(signal)

    def deactivate(self, signal):
        if signal in self.activate_signal:
            self.activate_signal.remove(signal)

    def is_activate(self, signal):
        return signal in self.activate_signal

    def start(self):
        logger = logging.getLogger('scape')
        logger.info('Scape started.')
        listener.signal(listener.SIGINT, lambda sig_id, handle: exit())
        while True:
            for signal in self.activate_signal:
                self.update_signal_status(signal)
                Recognizer.get_instance().process(signal)
            Dispatcher.get_instance().try_unlock()
