import abc
import time
import multiprocessing
from scape.action.action import Action, CompoundAction


class EventStream(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def put(self, event):
        pass


class ActionStream(EventStream):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__action_stream = multiprocessing.Queue()

    def get(self):
        return self.__action_stream.get()

    def put(self, action):
        self.__action_stream.put(action)


class RecorderStream(EventStream):
    def __init__(self, action_stream, name):
        self.__action_stream = action_stream
        self.record_action = CompoundAction(name)
        self.begin_time = time.time()

    def get(self):
        action = self.__action_stream.get()
        end_time = time.time()
        self.record_action.add_group([Action('Delayer.delay', (end_time - self.begin_time,)), action])
        return action

    def put(self, action):
        self.__action_stream.put(action)

    def get_record_acton(self):
        return self.record_action
