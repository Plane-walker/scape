from scape.core.core import Core


class Executor(Core):
    def __init__(self):
        super().__init__()

    def execute(self, action):
        action_func = getattr(self, action.get_name())
        if callable(action_func):
            action_func(*(action.get_args()))
