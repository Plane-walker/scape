from scape.core.slot import Slot


class Parser:
    def __init__(self):
        self.rules = {}

    def add_rule(self, signal, rule):
        self.rules[signal] = rule

    @staticmethod
    def get_status(signal, args):
        Slot.get_instance().get_status(signal, args)
