from scape.core.core import Core


class Sensor(Core):
    def __init__(self):
        super().__init__()

    def init_signal_status(self, signal):
        if signal.get_status() is not None:
            return
        signal_func = getattr(self, signal.get_name())
        status = signal_func(*(signal.get_args()))
        signal.init_status(status)

    def update_signal_status(self, signal):
        if signal.get_status() is None:
            raise
        signal_func = getattr(self, signal.get_name())
        status = signal_func(*(signal.get_args()))
        signal.update_status(status)
