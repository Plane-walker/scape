import os
import json
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


class CompoundEvent(metaclass=abc.ABCMeta):
    def __init__(self, name, store_path):
        self._name = name
        self._store_path = store_path
        with open(os.path.join(os.getcwd(), store_path), 'r') as f:
            events = json.load(f)
        if name not in events.keys():
            self._detail = []
        else:
            self._detail = events[name]

    @abc.abstractmethod
    def add_group(self, event_list):
        pass

    @abc.abstractmethod
    def deserialize(self):
        pass
