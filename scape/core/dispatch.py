import json
import importlib
import os
import multiprocessing
from scape.action.executor import Executor


class Dispatcher(multiprocessing.Process, Executor):
    def __init__(self, action_queue):
        super().__init__()
        self.action_queue = action_queue

    def run(self):
        while True:
            action_group = self.action_queue.get()
            for action in action_group:
                action[0](*(action[1]))


class DispatchPool:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, executors, pool_size):
        self.executors = {}
        for executor in executors:
            module, executor = executor.rsplit('.', 1)
            module = importlib.import_module(module)
            executor = getattr(module, executor)()
            self.executors[executor.__class__.__name__] = executor
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'r') as f:
            self.actions = json.load(f)
        self.action_queue = multiprocessing.Queue(pool_size)
        for index in range(pool_size):
            dispatcher = Dispatcher(self.action_queue)
            dispatcher.daemon = True
            dispatcher.start()

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def create_combine_action(self, name, *func_list):
        self.actions[name] = []
        for index in func_list:
            func_line = []
            for func, args in index:
                func_line.append(func.__name__)
                func_line.append(args)
            self.actions[name].append(func_line)
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'w') as f:
            json.dump(self.actions, f)

    def add_process(self, class_name, action_name, args):
        if class_name in self.executors.keys():
            func = getattr(self.executors[class_name], action_name)
            self.action_queue.put([(func, args)])

    def add_group_action(self, group_action):
        actions = []
        for action in group_action:
            class_name, action_name = action[0].split('.', 1)
            func = getattr(self.executors[class_name], action_name)
            actions.append((func, action[1]))
        self.action_queue.put(actions)

    def process(self, action_name, args):
        if action_name.find('.') != -1:
            class_name, action_name = action_name.split('.', 1)
            self.add_process(class_name, action_name, args)
        elif action_name in self.actions.keys():
            combine_action = self.actions[action_name]
            for group_action in combine_action:
                self.add_group_action(group_action)
