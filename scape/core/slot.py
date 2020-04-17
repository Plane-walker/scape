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

    def __init__(self, sensors, init_activate_signals):
        super().__init__()
        self.sensors = {}
        for sensor in sensors:
            module, sensor = sensor.rsplit('.', 1)
            module = importlib.import_module(module)
            sensor = getattr(module, sensor)()
            self.sensors[sensor.__class__.__name__] = sensor
        self.init_sensors()
        for signal in init_activate_signals:
            for arg in init_activate_signals[signal]:
                self.activate(signal, arg)

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def activate(self, signal, args):
        sensor_name, signal_name = signal.split('.', 1)
        signal = getattr(self.sensors[sensor_name], signal_name)
        self.sensors[sensor_name].activate(signal, args)

    def deactivate(self, signal, args):
        sensor_name, signal_name = signal.split('.', 1)
        signal = getattr(self.sensors[sensor_name], signal_name)
        self.sensors[sensor_name].deactivate(signal, args)

    def is_activate(self, signal_name, args):
        if signal_name.find('.') == -1:
            raise
        sensor, signal = signal_name.split('.', 1)
        if sensor not in self.sensors.keys():
            raise
        sensor = self.sensors[sensor]
        signal = getattr(sensor, signal)
        return sensor.is_activate(signal, args)

    def init_sensors(self):
        for sensor in self.sensors.values():
            for func in dir(sensor):
                if callable(getattr(sensor, func)) and re.match(SIGNAL_FUNC, getattr(sensor, func).__name__) is not None:
                    getattr(sensor, func)()
            sensor.INIT = True

    def start(self):
        while True:
            for sensor in self.sensors.values():
                for signal, args in sensor.get_loop_signals():
                    status = signal(*args)
                    func_name = signal.__name__.split('_signal_', 1)[1]
                    ParserPool.get_instance().process(sensor.__class__.__name__, func_name, args, status)

    def get_signal_args(self, signal_name):
        if signal_name.find('.') == -1:
            raise
        sensor, signal = signal_name.split('.', 1)
        if sensor not in self.sensors.keys():
            raise
        sensor = self.sensors[sensor]
        return sensor.get_signal_args(getattr(sensor, signal))

    def get_signal_status(self, signal_name, args):
        if signal_name.find('.') == -1:
            raise
        sensor, signal = signal_name.split('.', 1)
        if sensor not in self.sensors.keys():
            raise
        sensor = self.sensors[sensor]
        signal = getattr(sensor, signal)
        return sensor.get_signal_status(signal, args)


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

    def process(self, class_name, func_name, args, status):
        index_name = class_name + '.' + func_name
        if (index_name, args) in self.rules.keys():
            self.rules[(index_name, args)](args, status)
