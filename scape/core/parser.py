from scape.framework.dispatch import Dispatcher
from scape.core.core import Core


class Parser(Core):
    def __init__(self):
        super().__init__()
        self.rules = {}
        self.signal_count = {}
        self.__received_signal = None

    def add_rule(self, signal_list, rule):
        if not isinstance(signal_list, list):
            signal_list = [signal_list]
        for signal in signal_list:
            def rule_func(received_signal):
                self.__received_signal = received_signal
                rule()
            self.rules[signal] = rule_func

    def received_signal(self):
        return self.__received_signal

    @staticmethod
    def process(action, transaction=True):
        if action.get_block():
            return
        if transaction:
            action.set_block(True)
        Dispatcher.get_instance().process(action)
