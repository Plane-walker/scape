import json
import importlib
import os
import random
import multiprocessing
from .utils import func_to_str
from scape.action.executor import Executor


class Dispatcher(Executor, multiprocessing.Process):
    def __init__(self, executors):
        super().__init__()
        self.executors = {}
        for executor in executors:
            module, executor = executor.rsplit('.', 1)
            module = importlib.import_module(module)
            executor = getattr(module, executor)()
            self.executors[executor.__class__.__name__] = executor
        self.process_queue = []

    def add_process(self, class_name, action_name, args):
        if class_name in self.executors.keys():
            func = getattr(self.executors[class_name], action_name)
            self.process_queue.append((func, args))

    def run(self):
        while len(self.process_queue) > 0:
            func = self.process_queue.pop(0)
            func[0](*(func[1]))


class DispatchPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, executors, pool_size):
        self.executors = executors
        self.pool_size = pool_size
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'r') as f:
            self.actions = json.load(f)

    @classmethod
    def get_instance(cls):
        return cls._instance

    def create_combine_action(self, name, *func_list):
        self.actions[name] = []
        for index in func_list:
            func_line = []
            for func, args in index:
                func_line.append(func_to_str(func))
                func_line.append(args)
            self.actions[name].append(func_line)
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'w') as f:
            json.dump(self.actions, f)

    def process(self, action_name, args):
        dispatchers = []
        if action_name.find('.') != -1:
            class_name, action_name = action_name.split('.', 1)
            dispatcher = Dispatcher(self.executors)
            dispatcher.add_process(class_name, action_name, args)
            dispatchers.append(dispatcher)
        elif action_name in self.actions.keys():
            combine_action = self.actions[action_name]
            for group_action in combine_action:
                if len(dispatchers) < self.pool_size:
                    dispatcher = Dispatcher(self.executors)
                    dispatchers.append(dispatcher)
                else:
                    dispatcher = random.choice(dispatchers)
                for action in group_action:
                    class_name, action_name = action[0].split('.', 1)
                    dispatcher.add_process(class_name, action_name, action[1])
        for dispatcher in dispatchers:
            dispatcher.start()
        for dispatcher in dispatchers:
            dispatcher.join()
