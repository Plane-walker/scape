import importlib
import re
from scape.signal.sensor import Sensor
from scape.core.parser import ParserPool


SIGNAL_FUNC = '_signal_[_a-zA-Z0-9]*'


class Slot(Sensor):
    def __init__(self, sensors):
        super().__init__()
        self.sensors = {}
        for sensor in sensors:
            module, sensor = sensor.rsplit('.', 1)
            module = importlib.import_module(module)
            sensor = getattr(module, sensor)()
            self.sensors[sensor.__class__.__name__] = sensor

    def start(self):
        self.signal_recognize()
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
