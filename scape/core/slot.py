import importlib
from scape.signal.sensor import Sensor
from scape.core.parser import ParserPool
from .utils import func_to_str


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
        for sensor in self.sensors.values():
            for signal in sensor.loop_signals:
                signal[0](*(signal[1]))
        while True:
            for sensor in self.sensors.values():
                for signal in sensor.loop_signals:
                    old_status = sensor.get_status(signal[0])
                    new_status = signal[0](*(signal[1]))
                    if old_status is not new_status:
                        ParserPool.get_instance().process(sensor.__class__.__name__, func_to_str(signal[0]), old_status, new_status)
