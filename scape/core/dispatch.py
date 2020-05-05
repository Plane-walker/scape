import importlib
import multiprocessing
import time
from scape.action.executor import Executor
from scape.action.action import Action, CompoundAction, ActionFactory


class Dispatcher(multiprocessing.Process, Executor):
    def __init__(self, executors, action_queue, lock):
        super().__init__()
        self.executors = {}
        for executor in executors:
            module, executor = executor.rsplit('.', 1)
            module = importlib.import_module(module)
            executor = getattr(module, executor)()
            self.executors[executor.__class__.__name__] = executor
        self.action_queue = action_queue
        self.lock = lock
        self.action = None

    def execute(self, action):
        executor = action.get_processor_name()
        if executor not in self.executors.keys():
            raise
        self.executors[executor].execute(action)

    def run(self):
        while True:
            if self.action is None:
                self.action = self.action_queue.get()
            if isinstance(self.action, Action):
                self.execute(self.action)
                self.lock.acquire()
                self.action = self.action.activate_next()
                self.lock.release()
            elif isinstance(self.action, CompoundAction):
                object_parallel = self.action.deserialize()
                self.action = object_parallel[0][0]
                for action_group in object_parallel[1:]:
                    self.action_queue.put(action_group[0])


class DispatchPool:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, executors, pool_size):
        self.action_queue = multiprocessing.Queue(pool_size)
        executors.append('scape.action.utils.Delayer')
        for index in range(pool_size):
            dispatcher = Dispatcher(executors, self.action_queue, multiprocessing.Lock())
            dispatcher.daemon = True
            dispatcher.start()
        self.record_actions = None
        self.record = False
        self.begin_time = None
        self.end_time = None

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def start_record(self):
        self.record = True

    def stop_record(self, compound_action):
        self.record = False
        self.begin_time = None
        compound_action.add_group(*self.record_actions)
        self.record_actions = None
        return compound_action

    def process(self, action):
        if self.record:
            self.end_time = time.time()
            if self.begin_time is not None:
                self.record_actions.append(ActionFactory.make('Delayer.delay', (self.end_time - self.begin_time,)))
            self.record_actions.append(action)
        if isinstance(action, Action):
            self.action_queue.put(action)
        elif isinstance(action, CompoundAction):
            for action_group in action.deserialize():
                self.action_queue.put(action_group[0])
        if self.record and self.begin_time is None:
            self.begin_time = time.time()
