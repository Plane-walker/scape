import abc


class Sensor(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def init_signal_status(self, signal):
        pass

    @abc.abstractmethod
    def update_signal_status(self, signal):
        pass


class SignalSensor(Sensor):
    def __init__(self):
        super().__init__()

    def init_signal_status(self, signal):
        signal_func = getattr(self, signal.get_name())
        status = signal_func(*(signal.get_args()))
        signal.init_status(status)

    def update_signal_status(self, signal):
        signal_func = getattr(self, signal.get_name())
        status = signal_func(*(signal.get_args()))
        signal.update_status(status)
