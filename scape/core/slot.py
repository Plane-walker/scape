import importlib


class Slot:
    def __init__(self, dispatcher, senders):
        self.dispatcher = dispatcher
        self.senders = {}
        for sender in senders:
            module, sender = sender.rsplit('.', 1)
            module = importlib.import_module(module)
            sender = getattr(module, sender)()
            self.senders[sender.__class__.__name__] = sender

    def start(self):
        for sender in self.senders.values():
            for signal in sender.loop_signals:
                signal[0](*(signal[1]))
        while True:
            for sender in self.senders.values():
                for signal in sender.loop_signals:
                    old_status = sender.status[signal[0]]
                    new_status = signal[0](signal[1])
                    if old_status is not new_status:
                        self.dispatcher.dispatch(sender, signal[0], new_status)
