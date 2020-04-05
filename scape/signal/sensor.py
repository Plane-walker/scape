class Sensor:
    def __init__(self):
        pass


class SignalSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.status = {}
        self.loop_signals = {}

    def add_loop_signals(self, *signals):
        for signal in signals:
            self.loop_signals[signal[0]] = signal[1]

    def get_status(self, signal):
        if signal in self.status.keys():
            return self.status[signal]
        raise
