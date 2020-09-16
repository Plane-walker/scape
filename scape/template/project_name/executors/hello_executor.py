from scape.core.executor import Executor


class HelloExecutor(Executor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def print_to_screen(status):
        print(status)
