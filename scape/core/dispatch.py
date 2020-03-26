import json
import importlib
import os
from .utils import func_to_str


class Dispatcher:
    def __init__(self, executors, centers):
        self.executors = {}
        self.centers = {}
        for executor in executors:
            module, executor = executor.rsplit('.', 1)
            module = importlib.import_module(module)
            executor = getattr(module, executor)()
            self.executors[executor.__class__.__name__] = executor
        for center in centers:
            module, center = center.rsplit('.', 1)
            module = importlib.import_module(module)
            center = getattr(module, center)()
            self.executors[center.__class__.__name__] = center
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'r') as f:
            self.combine_actions = json.load(f)

    def dispatch(self, sender, signal, status):
        if signal in sender.process_signal_center.keys():
            self.centers[sender.process_signal_center[signal]].process(signal, status)
        else:
            for center in sender.process_center:
                self.centers[center].try_process(signal, status)

    def create_combine_action(self, name, *func_list):
        self.combine_actions[name] = []
        for index in func_list:
            func_line = []
            for func, args in index:
                func_line.append(func_to_str(func))
                func_line.append(args)
            self.combine_actions[name].append(func_line)
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'w') as f:
            json.dump(self.combine_actions, f)
