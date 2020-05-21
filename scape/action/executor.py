import abc


class Executor(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self, action):
        pass


class ActionExecutor(Executor):
    def __init__(self):
        super().__init__()

    def execute(self, action):
        action_func = getattr(self, action.get_name())
        if callable(action_func):
            return action_func(*(action.get_args()))
