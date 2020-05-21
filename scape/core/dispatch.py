import importlib
import multiprocessing
import time
from scape.action.executor import Executor
from scape.conf.settings import INNER_EXECUTORS
from scape.action.action import Action, CompoundAction, ActionFactory
from scape.stream.action_stream import ActionStream


class Dispatcher(multiprocessing.Process, Executor):
    def __init__(self, executors, action_stream, lock, stream_info):
        super().__init__()
        self.executors = {}
        for executor in executors:
            module, executor = executor.rsplit('.', 1)
            module = importlib.import_module(module)
            executor = getattr(module, executor)()
            self.executors[executor.__class__.__name__] = executor
        self.action_stream = action_stream
        self.lock = lock
        self.action = None
        self.stream_info = stream_info

    def execute(self, action):
        executor = action.get_processor_name()
        if executor not in self.executors.keys():
            raise
        self.executors[executor].execute(action)

    def run(self):
        while True:
            if self.stream_info['current_stream'] is not self.action_stream:
                self.action_stream = self.stream_info['current_stream']
            if self.action is None:
                self.action = self.action_stream.get()
            if isinstance(self.action, Action):
                self.execute(self.action)
                self.lock.acquire()
                self.action = self.action.activate_next()
                self.lock.release()
            elif isinstance(self.action, CompoundAction):
                object_parallel = self.action.deserialize()
                self.action = object_parallel[0][0]
                for action_group in object_parallel[1:]:
                    self.action_stream.put(action_group[0])


class DispatchPool:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, executors, pool_size):
        self.inner_executors = {}
        for executor in INNER_EXECUTORS:
            module, executor = executor.rsplit('.', 1)
            module = importlib.import_module(module)
            executor = getattr(module, executor)()
            self.inner_executors[executor.__class__.__name__] = executor
        self.action_stream = ActionStream()
        self.stream_info = {'current_stream': self.action_stream}
        for index in range(pool_size):
            dispatcher = Dispatcher(executors, self.action_stream, multiprocessing.Lock(), self.stream_info)
            dispatcher.daemon = True
            dispatcher.start()

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def process(self, action):
        if isinstance(action, Action):
            executor = action.get_processor_name()
            if executor in self.inner_executors.keys():
                return self.inner_executors[executor].execute(action)
        if isinstance(action, Action):
            self.action_stream.put(action)
        elif isinstance(action, CompoundAction):
            for action_group in action.deserialize():
                self.action_stream.put(action_group[0])

    def change_stream(self, new_stream):
        self.stream_info['current_stream'] = new_stream

    def get_current_stream(self):
        return self.stream_info['current_stream']
