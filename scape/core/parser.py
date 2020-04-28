from scape.core.slot import Slot
from scape.core.dispatch import DispatchPool


class Parser:
    def __init__(self):
        self.rules = {}
        self.signal_count = {}
        self.__received_signal = None

    def add_rule(self, signal_list, rule):
        if not isinstance(signal_list, list):
            signal_list = [signal_list]
        for signal in signal_list:
            def rule_func(received_signal):
                self.__received_signal = received_signal
                result = rule()
                if result is not None:
                    action = result
                    return DispatchPool.get_instance().process(action)
            self.rules[signal] = rule_func

    def init_activate(self, *signal_list):
        for signal in signal_list:
            self.activate(signal)

    def received_signal(self):
        return self.__received_signal

    @staticmethod
    def activate(signal):
        return Slot.get_instance().activate(signal)

    @staticmethod
    def deactivate(signal):
        return Slot.get_instance().deactivate(signal)

    @staticmethod
    def is_activate(signal):
        return Slot.get_instance().is_activate(signal)
