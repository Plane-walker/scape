import time
from scape.action.executor import ActionExecutor
from scape.core.slot import Slot


class InnerExecutor(ActionExecutor):
    def __init__(self):
        super().__init__()


class Delayer(InnerExecutor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def delay(secs):
        time.sleep(secs)


class Activator(InnerExecutor):
    def __init__(self):
        super().__init__()

    def init_activate(self, *signal_list):
        for signal in signal_list:
            self.activate(signal)

    @staticmethod
    def activate(signal):
        return Slot.get_instance().activate(signal)

    @staticmethod
    def deactivate(signal):
        return Slot.get_instance().deactivate(signal)

    @staticmethod
    def is_activate(signal):
        return Slot.get_instance().is_activate(signal)
