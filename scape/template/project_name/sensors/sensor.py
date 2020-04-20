from scape.signal.sensor import SignalSensor
from scape.signal.decorators import signal_func


class SensorDemo(SignalSensor):
    def __init__(self):
        super().__init__()

    @signal_func(())
    def signal(self):
        return 'say hello'
