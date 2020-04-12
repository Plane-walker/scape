class Sensor:
    def __init__(self):
        pass


class SignalSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.__new_status = {}
        self.__old_status = {}
        self.__loop_signals = []

    def _update_status(self, signal, args):
        if not callable(signal):
            raise
        status = signal(self, *args)
        if (signal.__name__, args) in self.__new_status.keys():
            self.__old_status[(signal.__name__, args)] = self.__new_status[(signal.__name__, args)]
        else:
            self.__old_status[(signal.__name__, args)] = None
        self.__new_status[(signal.__name__, args)] = status

    def add_loop_signal(self, signal):
        self.__loop_signals.append(signal)

    def get_old_status(self, signal, args):
        if (signal.__name__, args) not in self.__old_status.keys():
            raise
        return self.__old_status[(signal.__name__, args)]

    def get_new_status(self, signal, args):
        if (signal.__name__, args) not in self.__new_status.keys():
            raise
        return self.__new_status[(signal.__name__, args)]

    def get_loop_signals(self):
        return self.__loop_signals
