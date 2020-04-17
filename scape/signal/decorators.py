from functools import wraps


__all__ = ['signal_func']


def signal_func(*signal_args):
    def get_signal(signal):
        signal.__name__ = '_signal_' + signal.__name__
        @wraps(signal)
        def signals(self, *args):
            if not self.INIT:
                for arg in signal_args:
                    self.init_signal_status(signal, arg)
                return
            return self.update_signal_status(signal, args)
        return signals
    return get_signal
