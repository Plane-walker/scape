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
                if received_signal.is_lock():
                    return
                self.__received_signal = received_signal
                rule()
            self.rules[signal] = rule_func

    def received_signal(self):
        return self.__received_signal

    def process(self, action, transaction=False):
        if transaction:
            self.__received_signal.lock()
            action.add_locked_signal(self.__received_signal)
        return DispatchPool.get_instance().process(action)
