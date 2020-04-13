from scape.core.slot import Slot


class Parser:
    def __init__(self):
        self.rules = {}
        self.signal_count = {}

    def add_rule(self, signal, rule):
        if type(signal) is str:
            args = Slot.get_instance().get_signal_args(signal)
            for arg in args:
                self.rules[(signal, arg)] = rule
        else:
            self.rules[signal] = rule

    def add_multi_signal_rule(self, signal, rule):
        if type(signal) is str:
            args = Slot.get_instance().get_signal_args(signal)
            for arg in args:
                self.rules[(signal, arg)] = rule
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
