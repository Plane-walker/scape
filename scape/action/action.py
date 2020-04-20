import os
import json


class Action:
    def __init__(self, name, args):
        if name.find('.') == -1:
            raise
        self.__executor, self.__name = name.split('.', 1)
        self.__args = args

    def get_executor_name(self):
        return self.__executor

    def get_name(self):
        return self.__name

    def get_args(self):
        return self.__args

    def serialize(self):
        return [self.__executor + '.' + self.__name, self.__args]

    def execute(self, executor):
        executor.execute([self.__name, self.__args])


class CompoundAction:
    def __init__(self, action_name):
        self.__action_name = action_name
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'r') as f:
            actions = json.load(f)
        if action_name not in actions.keys():
            self.__action_detail = []
        else:
            self.__action_detail = actions[action_name]

    def add_group(self, action_list):
        action_group = []
        for action_obj in action_list:
            action_group.append(action_obj.serialize())
        self.__action_detail.append(action_group)
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'rw') as f:
            actions = json.load(f)
            actions[self.__action_name] = self.__action_detail
            json.dump(actions, f)

    def deserialize(self):
        object_parallel = []
        for action_group in self.__action_detail:
            action_list = []
            for action in action_group:
                action_list.append(Action(action[0], action[1]))
            object_parallel.append(action_list)
        return object_parallel
