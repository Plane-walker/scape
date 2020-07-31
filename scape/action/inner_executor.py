import time
from scape.action.executor import ActionExecutor
from scape.core.slot import Slot
from scape.core.dispatch import DispatchPool
from scape.stream.stream import RecorderStream


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


class Recorder(InnerExecutor):
    def __init__(self):
        super().__init__()
        self.store_stream = None

    def start(self, name):
        self.store_stream = DispatchPool.get_instance().get_current_stream()
        DispatchPool.get_instance().change_stream(RecorderStream(self.store_stream, name))

    def end(self):
        record_action = DispatchPool.get_instance().get_current_stream().get_record_action()
        DispatchPool.get_instance().change_stream(self.store_stream)
        return record_action
