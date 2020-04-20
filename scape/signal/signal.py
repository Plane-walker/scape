import os
import json


from scape.core.event import Event, CompoundEvent


class Signal(Event):
    def __init__(self, name, args):
        super().__init__(name, args)


class CompoundSignal(CompoundEvent):
    def __init__(self, name):
        super().__init__(name, 'conf/compound_signal.json')
        self._signal_list = []

    def add_group(self, signal_list):
        for signal_obj in signal_list:
            self._detail.append(signal_obj.serialize())
        with open(os.path.join(os.getcwd(), self._store_path), 'rw') as f:
            actions = json.load(f)
            actions[self._name] = self._detail
            json.dump(actions, f)

    def deserialize(self):
        if len(self._signal_list) == 0:
            for signal in self._detail:
                self._signal_list.append(Signal(signal[0], signal[1]))
        return self._signal_list
