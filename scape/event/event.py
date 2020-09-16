import abc


class Event(metaclass=abc.ABCMeta):
    def __init__(self, name, args):
        if name.find('.') == -1:
            raise
        self._processor, self._name = name.split('.', 1)
        self._args = args

    def get_processor_name(self):
        return self._processor

    def get_name(self):
        return self._name

    def get_args(self):
        return self._args

    def serialize(self):
        return [self._processor + '.' + self._name, self._args]


class EventFactory(metaclass=abc.ABCMeta):
    event_store = {}

    @classmethod
    def make(cls, name, *args):
        if (name, args) in cls.event_store:
            return cls.event_store[(name, args)]
        event = cls.init_event(name, args)
        cls.event_store[(name, args)] = event
        return event

    @classmethod
    @abc.abstractmethod
    def init_event(cls, name, args):
        pass
