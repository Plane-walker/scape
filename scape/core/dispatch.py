import importlib
import multiprocessing
from scape.action.executor import Executor
from scape.core.compound_action import CompoundAction


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

    def execute(self, action, args):
        if action.find('.') == -1:
            raise
        executor, action = action.split('.', 1)
        if executor not in self.executors.keys():
            raise
        self.executors[executor].execute(action, args)

    def run(self):
        while True:
            action_group = self.action_queue.get()
            for action in action_group:
                self.lock.acquire()
                if action not in self.action_name:
                    self.action_name.append(action)
                    self.lock.release()
                    self.execute(action[0], action[1])
                    self.lock.acquire()
                    self.action_name.remove(action)
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

    def process(self, action_name, args):
        if action_name.find('.') != -1:
            self.action_queue.put([(action_name, args)])
        else:
            compound_action = CompoundAction(action_name)
            for group_action in compound_action.parallel():
                self.action_queue.put(group_action)
