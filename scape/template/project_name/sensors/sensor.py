from scape.signal.sensor import SignalSensor


class SensorDemo(SignalSensor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def signal_0():
        return 'say'

    @staticmethod
    def signal_1():
        return 'hello'
