import os
import json
from scape.core.event import Event, CompoundEvent


class Action(Event):
    def __init__(self, name, args):
        super().__init__(name, args)


class CompoundAction(CompoundEvent):
    def __init__(self, name):
        super().__init__(name, 'conf/compound_action.json')

    def add_group(self, action_list):
        action_group = []
        for action_obj in action_list:
            action_group.append(action_obj.serialize())
        self._detail.append(action_group)
        with open(os.path.join(os.getcwd(), self._store_path), 'rw') as f:
            actions = json.load(f)
            actions[self._name] = self._detail
            json.dump(actions, f)

    def deserialize(self):
        object_parallel = []
        for action_group in self._detail:
            action_list = []
            for action in action_group:
                action_list.append(Action(action[0], action[1]))
            object_parallel.append(action_list)
        return object_parallel
