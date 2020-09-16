from scape.event.event import Event, EventFactory


_all__ = ['Signal', 'SignalFactory']


class Signal(Event):
    def __init__(self, name, args):
        super().__init__(name, args)
        self.__status = None

    def init_status(self, status):
        self.__status = {'old': status, 'new': status}

    def update_status(self, status):
        self.__status['old'] = self.__status['new']
        self.__status['new'] = status

    def get_status(self):
        return self.__status

    def rising_edge(self):
        if self.__status['old'] == 0 and self.__status['new'] == 1:
            return True
        return False

    def is_status(self, status):
        return status == self.__status['new']


class SignalFactory(EventFactory):
    @classmethod
    def init_event(cls, name, args):
        return Signal(name, args)
