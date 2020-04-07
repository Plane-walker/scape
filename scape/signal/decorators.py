def store_status(signal):
    def stored(self, *args, **kwargs):
        status = signal(self, *args, **kwargs)
        if status is not None:
            self.stauts[(signal, args, kwargs)] = status
        return self.stauts[signal]
    return stored
