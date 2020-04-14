from functools import wraps


def signal_func(*signal_args):
    def get_signal(signal):
        signal.__name__ = '_signal_' + signal.__name__
        @wraps(signal)
        def signals(self, *args):
            if not self.init:
                for arg in signal_args:
                    self.init_status(signal, arg)
                return
            return self.update_status(signal, args)
        return signals
    return get_signal
