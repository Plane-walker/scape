import importlib
import multiprocessing
from scape.action.executor import Executor
from scape.action.action import Action, CompoundAction


class Dispatcher(multiprocessing.Process, Executor):
    def __init__(self, executors, action_queue, lock, action_name):
        super().__init__()
        self.action_queue = action_queue
        self.lock = lock
        self.action_name = action_name
        self.executors = {}
        for executor in executors:
            module, executor = executor.rsplit('.', 1)
            module = importlib.import_module(module)
            executor = getattr(module, executor)()
            self.executors[executor.__class__.__name__] = executor

    def execute(self, action):
        executor = action.get_processor_name()
        if executor not in self.executors.keys():
            raise
        self.executors[executor].execute(action)

    def run(self):
        while True:
            action_group = self.action_queue.get()
            for action in action_group:
                self.lock.acquire()
                if action.serialize() not in self.action_name:
                    self.action_name.append(action.serialize())
                    self.lock.release()
                    self.execute(action)
                    self.lock.acquire()
                    self.action_name.remove(action.serialize())
                    self.lock.release()
                else:
                    self.lock.release()


class DispatchPool:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, executors, pool_size):
        self.action_queue = multiprocessing.Queue(pool_size)
        self.lock = multiprocessing.Lock()
        self.action_name = []
        for index in range(pool_size):
            dispatcher = Dispatcher(executors, self.action_queue, self.lock, self.action_name)
            dispatcher.daemon = True
            dispatcher.start()

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def process(self, action):
        if isinstance(action, Action):
            self.action_queue.put([action])
        elif isinstance(action, CompoundAction):
            for action_group in action.deserialize():
                self.action_queue.put(action_group)
