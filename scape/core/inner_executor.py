import time
from scape.core.executor import Executor
from scape.framework.receive import Receiver
from scape.framework.dispatch import Dispatcher
from scape.stream.stream import RecorderStream


class InnerExecutor(Executor):
    def __init__(self):
        super().__init__()


class Delayer(Executor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def delay(secs):
        time.sleep(secs)


class Activator(Executor):
    def __init__(self):
        super().__init__()

    def init_activate(self, *signal_list):
        for signal in signal_list:
            self.activate(signal)

    @staticmethod
    def activate(signal):
        Receiver.get_instance().activate(signal)

    @staticmethod
    def deactivate(signal):
        Receiver.get_instance().deactivate(signal)

    @staticmethod
    def is_activate(signal):
        return Receiver.get_instance().is_activate(signal)


class Recorder(InnerExecutor):
    def __init__(self):
        super().__init__()
        self.store_stream = None

    def start(self):
        self.store_stream = Dispatcher.get_instance().get_current_stream()
        Dispatcher.get_instance().change_stream(RecorderStream(self.store_stream))

    def end(self):
        record_action = Dispatcher.get_instance().get_current_stream().get_record_action()
        Dispatcher.get_instance().change_stream(self.store_stream)
        return record_action
