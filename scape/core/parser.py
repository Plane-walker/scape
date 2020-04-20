from scape.core.slot import Slot
from scape.core.dispatch import DispatchPool


class Parser:
    def __init__(self):
        self.rules = {}
        self.signal_count = {}

    def add_rule(self, signal, rule):
        def rule_func(*rule_args):
            result = rule(*rule_args)
            if result is not None:
                action = result
                return DispatchPool.get_instance().process(action)
        self.rules[signal] = rule_func

    def init_activate(self, *signal_list):
        for signal in signal_list:
            self.activate(signal)

    @staticmethod
    def get_signal_status(signal):
        return Slot.get_instance().get_signal_status(signal)

    @staticmethod
    def activate(signal):
        return Slot.get_instance().activate(signal)

    @staticmethod
    def deactivate(signal):
        return Slot.get_instance().deactivate(signal)

    @staticmethod
    def is_activate(signal):
        return Slot.get_instance().is_activate(signal)
