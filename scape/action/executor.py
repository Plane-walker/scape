import abc


class Executor:
    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self, action, args):
        pass


class ActionExecutor(Executor):
    def __init__(self):
        super().__init__()

    def execute(self, action, args):
        action = getattr(self, action)
        if callable(action):
            action(*args)
