from functools import wraps


def signal_func(*args):
    def get_func(func):
        func.__name__ = '_signal_' + func.__name__
        @wraps(func)
        def signals(self):
            for arg in args:
                self._update_status(func, arg)
            return args
        return signals
    return get_func


def no_loop_signal_func(*args):
    def get_func(func):
        func.__name__ = '_no_loop_signal_' + func.__name__
        @wraps(func)
        def signals(self):
            for arg in args:
                self._update_status(func, arg)
            return args
        return signals
    return get_func

