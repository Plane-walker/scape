import os
import json


__all__ = ['Signal', 'CompoundSignal', 'SignalFactory']

from scape.core.event import Event, CompoundEvent, EventFactory


class Signal(Event):
    def __init__(self, name, args):
        super().__init__(name, args)
        self.__status = {}
        self.__signal_lock = 0

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

    def has_status(self, status):
        return status == self.__status['new']

    def lock(self):
        self.__signal_lock = 1

    def unlock(self):
        self.__signal_lock = 0

    def is_lock(self):
        return self.__signal_lock == 1


class CompoundSignal(CompoundEvent):
    def __init__(self, name):
        super().__init__(name, 'conf/compound_signal.json')
        self._signal_list = []

    def add_group(self, signal_list):
        for signal_obj in signal_list:
            self._detail.append(signal_obj.serialize())
        with open(os.path.join(os.getcwd(), self._store_path), 'r') as f:
            actions = json.load(f)
        with open(os.path.join(os.getcwd(), self._store_path), 'w') as f:
            actions[self._name] = self._detail
            json.dump(actions, f)

    def deserialize(self):
        if len(self._signal_list) == 0:
            for signal in self._detail:
                self._signal_list.append(Signal(signal[0], signal[1]))
        return self._signal_list

    def get_status(self):
        signals = self.deserialize()
        return [signal.get_status() for signal in signals]

    def lock(self):
        for signal in self._signal_list:
            signal.lock()

    def unlock(self):
        for signal in self._signal_list:
            signal.unlock()

    def is_lock(self):
        for signal in self._signal_list:
            if signal.is_lock() == 1:
                return 1
        return 0


class SignalFactory(EventFactory):
    @classmethod
    def init_event(cls, name, args):
        return Signal(name, args)

    @classmethod
    def init_compound_event(cls, name):
        return CompoundSignal(name)
