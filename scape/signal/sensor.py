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

    @abc.abstractmethod
    def get_signal_status(self, signal):
        pass


class SignalSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.__status = {}
        self.__loop_signals = []
        self.INIT = False

    def init_signal_status(self, signal):
        signal_func = getattr(self, signal.get_name())
        status = signal_func(*(signal.get_args()))
        self.__status[signal] = {'old': status, 'new': status}
        return self.__status[signal]

    def update_signal_status(self, signal):
        self.__status[signal]['old'] = self.__status[signal]['new']
        signal_func = getattr(self, signal.get_name())
        self.__status[signal]['new'] = signal_func(*(signal.get_args()))
        return self.__status[signal]

    def get_signal_status(self, signal):
        if signal not in self.__status:
            raise
        return self.__status[signal]
