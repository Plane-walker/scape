import os
import json


class CompoundAction:
    def __init__(self, action_name):
        self.__action_name = action_name
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'r') as f:
            actions = json.load(f)
        if action_name not in actions.keys():
            self.__action_detail = []
        else:
            self.__action_detail = actions[action_name]

    def add_group(self, *func_list):
        action_group = []
        for func in func_list:
            action_group.append(func)
        self.__action_detail.append(action_group)
        with open(os.path.join(os.getcwd(), 'conf/action.json'), 'rw') as f:
            actions = json.load(f)
            actions[self.__action_name] = self.__action_detail
            json.dump(actions, f)

    def parallel(self):
        return self.__action_detail
