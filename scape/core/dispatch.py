import json
from .utils import func_to_str


class Dispatcher:
    def __init__(self, executors):
        self.executors = {}
        for executor in executors:
            self.executors[executor.__class__.__name__] = executor
        with open('action.json', 'r') as f:
            self.combine_actions = json.load(f)

    @staticmethod
    def dispatch(sender, signal, status):
        if signal in sender.process_signal_center.keys():
            sender.process_signal_center[signal].process(signal, status)
        else:
            for center in sender.process_center:
                center.try_process(signal, status)

    def create_combine_action(self, name, *func_list):
        self.combine_actions[name] = []
        for index in func_list:
            func_line = []
            for func, args in index:
                func_line.append(func_to_str(func))
                func_line.append(args)
            self.combine_actions[name].append(func_line)
        with open('action.json', 'w') as f:
            json.dump(self.combine_actions, f)
