import importlib
import re
from scape.signal.sensor import Sensor


SIGNAL_FUNC = '_signal_[_a-zA-Z0-9]*'


class Slot(Sensor):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, sensors):
        super().__init__()
        self.sensors = {}
        for sensor in sensors:
            module, sensor = sensor.rsplit('.', 1)
            module = importlib.import_module(module)
            sensor = getattr(module, sensor)()
            self.sensors[sensor.__class__.__name__] = sensor
        self.signal_recognize()

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def start(self):
        while True:
            for sensor in self.sensors.values():
                for signal in sensor.get_loop_signals():
                    args_list = signal()
                    for args in args_list:
                        old_status = sensor.get_old_status(signal, args)
                        new_status = sensor.get_new_status(signal, args)
                        func_name = signal.__name__.split('_signal_', 1)[1]
                        ParserPool.get_instance().process(sensor.__class__.__name__, func_name, args, old_status, new_status)

    def signal_recognize(self):
        for sensor in self.sensors.values():
            for func in dir(sensor):
                if callable(getattr(sensor, func)) and re.match(SIGNAL_FUNC, getattr(sensor, func).__name__) is not None:
                    sensor.add_loop_signal(getattr(sensor, func))
                    getattr(sensor, func)()
                    getattr(sensor, func)()

    def get_signal_args(self, signal_name):
        if signal_name.find('.') == -1:
            raise
        sensor, signal = signal_name.split('.', 1)
        if sensor not in self.sensors.keys():
            raise
        sensor = self.sensors[sensor]
        return getattr(sensor, signal)()

    def get_status(self, signal_name, args):
        if signal_name.find('.') == -1:
            raise
        sensor, signal = signal_name.split('.', 1)
        if sensor not in self.sensors.keys():
            raise
        sensor = self.sensors[sensor]
        signal = getattr(sensor, signal)
        old_status = sensor.get_old_status(signal, args)
        new_status = sensor.get_new_status(signal, args)
        return {'old': old_status, 'new': new_status}


class ParserPool:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def __init__(self, parsers):
        self.parsers = {}
        self.rules = {}
        for parser in parsers:
            module, parser = parser.rsplit('.', 1)
            module = importlib.import_module(module)
            parser = getattr(module, parser)()
            self.parsers[parser.__class__.__name__] = parser
            self.rules.update(parser.rules)

    def process(self, class_name, func_name, args, old_status, new_status):
        index_name = class_name + '.' + func_name
        if (index_name, args) in self.rules.keys():
            self.rules[(index_name, args)](args, {'old': old_status, 'new': new_status})
