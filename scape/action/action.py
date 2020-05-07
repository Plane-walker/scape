import os
import json
from scape.core.event import Event, CompoundEvent, EventFactory


__all__ = ['Action', 'CompoundAction', 'ActionFactory']


class Action(Event):
    def __init__(self, name, args):
        super().__init__(name, args)
        self.__active = False
        self.__next_action = None

    def set_next(self, action):
        self.__next_action = action

    def is_activate(self):
        return self.__active

    def activate(self):
        self.__active = True

    def activate_next(self):
        if self.__next_action is None or self.__next_action.is_activate():
            return None
        self.__next_action.activate()
        return self.__next_action


class CompoundAction(CompoundEvent):
    def __init__(self, name):
        super().__init__(name, 'conf/compound_action.json')
        self.__active = False
        self.__next_action = None

    def add_group(self, action_list):
        action_group = []
        for action_obj in action_list:
            action_group.append(action_obj.serialize())
        self._detail.append(action_group)
        with open(os.path.join(os.getcwd(), self._store_path), 'r') as f:
            actions = json.load(f)
        with open(os.path.join(os.getcwd(), self._store_path), 'w') as f:
            actions[self._name] = self._detail
            json.dump(actions, f)

    def deserialize(self):
        object_parallel = []
        for action_list in self._detail:
            action_group = []
            for action_json in action_list:
                action = ActionFactory.make(action_json[0], tuple(action_json[1]))
                if len(action_group) != 0:
                    action_group[-1].set_next(action)
                action_group.append(action)
            object_parallel.append(action_group)
        for action_group in object_parallel:
            action_group[-1].set_next(self.__next_action)
        return object_parallel

    def set_next(self, action):
        self.__next_action = action

    def is_activate(self):
        return self.__active

    def activate(self):
        self.__active = True


class ActionFactory(EventFactory):
    @classmethod
    def make(cls, name, args=None):
        if args is not None:
            return cls.init_event(name, args)
        return cls.init_compound_event(name)

    @classmethod
    def init_event(cls, name, args):
        return Action(name, args)

    @classmethod
    def init_compound_event(cls, name):
        return CompoundAction(name)
