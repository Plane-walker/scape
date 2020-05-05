import time
from scape.action.executor import ActionExecutor


class Delayer(ActionExecutor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def delay(secs):
        time.sleep(secs)
