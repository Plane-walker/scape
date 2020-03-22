def store_status(signal):
    def stored(self, *args, **kwargs):
        self.stauts[signal] = signal(self, *args, **kwargs)
    return stored
