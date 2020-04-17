import abc


class Sensor(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def activate(self, signal, args):
        pass

    @abc.abstractmethod
    def deactivate(self, signal, args):
        pass

    @abc.abstractmethod
    def is_activate(self, signal, args):
        pass


class SignalSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.__status = {}
        self.__loop_signals = []
        self.INIT = False

    def activate(self, signal, args):
        self.__loop_signals.append((signal, args))

    def deactivate(self, signal, args):
        self.__loop_signals.remove((signal, args))

    def is_activate(self, signal, args):
        return (signal.__name__, args) in self.__loop_signals

    def init_signal_status(self, signal, args):
        status = signal(self, *args)
        self.__status[(signal.__name__, args)] = {'old': status, 'new': status}
        return self.__status[(signal.__name__, args)]

    def update_signal_status(self, signal, args):
        self.__status[(signal.__name__, args)]['old'] = self.__status[(signal.__name__, args)]['new']
        self.__status[(signal.__name__, args)]['new'] = signal(self, *args)
        return self.__status[(signal.__name__, args)]

    def get_signal_status(self, signal, args):
        if (signal.__name__, args) not in self.__status.keys():
            raise
        return self.__status[(signal.__name__, args)]

    def get_loop_signals(self):
        return self.__loop_signals

    def get_signal_args(self, signal):
        args = []
        for signal_name, arg in self.__status.keys():
            if signal_name == signal.__name__:
                args.append(arg)
        return args
