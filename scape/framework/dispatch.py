import importlib
import multiprocessing
from scape.conf.settings import INNER_EXECUTORS
from scape.event.action import ActionFactory
from scape.stream.stream import ActionStream, CompleteStream


class DispatcherThread(multiprocessing.Process):
    def __init__(self, executors, action_stream, complete_stream, stream_info):
        super().__init__()
        self.executors = {}
        for executor in executors:
            module, executor = executor.rsplit('.', 1)
            module = importlib.import_module(module)
            executor = getattr(module, executor)()
            self.executors[executor.__class__.__name__] = executor
        self.action_stream = action_stream
        self.complete_stream = complete_stream
        self.action = None
        self.stream_info = stream_info

    def execute(self, action):
        executor = action.get_processor_name()
        if executor not in self.executors.keys():
            raise
        self.executors[executor].execute(action)
        if action.get_block():
            self.complete_stream.put(action.serialize())

    def run(self):
        while True:
            if self.action_stream is not self.stream_info['current_stream']:
                self.action_stream = self.stream_info['current_stream']
            if self.action is None:
                self.action = self.action_stream.get()
            self.execute(self.action)
            self.action = None


class Dispatcher:
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
        self.complete_stream = CompleteStream()
        self.stream_info = {'current_stream': self.action_stream}
        for index in range(pool_size):
            dispatcher = DispatcherThread(executors, self.action_stream, self.complete_stream, self.stream_info)
            dispatcher.daemon = True
            dispatcher.start()

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def process(self, action):
        executor = action.get_processor_name()
        if executor in self.inner_executors.keys():
            self.inner_executors[executor].execute(action)
            return
        self.action_stream.put(action)

    def try_unlock(self):
        if not self.complete_stream.empty():
            name, args = self.complete_stream.get()
            ActionFactory.make(name, args).set_block(False)

    def change_stream(self, new_stream):
        self.stream_info['current_stream'] = new_stream

    def get_current_stream(self):
        return self.stream_info['current_stream']
