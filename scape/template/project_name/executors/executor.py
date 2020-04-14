from scape.action.executor import ActionExecutor


class ExecutorDemo(ActionExecutor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def print_to_screen(status):
        print(status)
