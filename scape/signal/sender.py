class Sender:
    def __init__(self):
        self.status = {}
        self.loop_signals = {}
        self.process_center = []
        self.process_signal_center = {}

    def add_loop_signals(self, *signals):
        for signal in signals:
            self.loop_signals[signal[0]] = signal[1]

    def add_process_center(self, *centers):
        for center in centers:
            if isinstance(center, tuple):
                self.process_signal_center[center[0]] = center[1]
            else:
                self.process_center.append(center)

    def get_status(self, signal):
        if signal in self.status.keys():
            return self.status[signal]
        raise
