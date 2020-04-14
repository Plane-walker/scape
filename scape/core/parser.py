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
                action_name, action_args = result
                return DispatchPool.get_instance().process(action_name, action_args)
        if type(signal) is str:
            args = Slot.get_instance().get_signal_args(signal)
            for arg in args:
                self.rules[(signal, arg)] = rule_func
        else:
            self.rules[signal] = rule

    def add_multi_signal_rule(self, signal, rule):
        def rule_func(*rule_args):
            if rule.__name__ in self.signal_count.keys():
                self.signal_count[rule.__name__][0] += 1
                self.signal_count[rule.__name__][0] %= self.signal_count[rule.__name__][1]
            if rule.__name__ not in self.signal_count.keys() or self.signal_count[rule.__name__][0] == 0:
                result = rule(*rule_args)
                if result is not None:
                    action_name, action_args = result
                    return DispatchPool.get_instance().process(action_name, action_args)
        if type(signal) is str:
            args = Slot.get_instance().get_signal_args(signal)
            for arg in args:
                self.rules[(signal, arg)] = rule_func
            if rule.__name__ not in self.signal_count.keys():
                self.signal_count[rule.__name__] = [0, len(args)]
            else:
                self.signal_count[rule.__name__][1] += len(args)
        else:
            self.rules[signal] = rule
            if rule.__name__ not in self.signal_count.keys():
                self.signal_count[rule.__name__] = [0, 1]
            else:
                self.signal_count[rule.__name__][1] += 1

    @staticmethod
    def get_status(signal, args):
        return Slot.get_instance().get_status(signal, args)

    @staticmethod
    def signal_status(signal, args):
        return Slot.get_instance().is_activate(signal, args)

    @staticmethod
    def deactivate(signal, args):
        return Slot.get_instance().deactivate(signal, args)

    @staticmethod
    def activate(signal, args):
        return Slot.get_instance().activate(signal, args)
