import abc
import time
import multiprocessing
from scape.event.action import Action


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

    def empty(self):
        return self.__action_stream.empty()


class CompleteStream(EventStream):
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

    def empty(self):
        return self.__action_stream.empty()


class RecorderStream(EventStream):
    def __init__(self, action_stream):
        self.__action_stream = action_stream
        self.record_action_group = []
        self.begin_time = time.time()

    def get(self):
        action = self.__action_stream.get()
        end_time = time.time()
        self.record_action_group.extend([Action('Delayer.delay', (end_time - self.begin_time,)), action])
        return action

    def put(self, action):
        self.__action_stream.put(action)

    def get_record_acton(self):
        return self.record_action_group

    def empty(self):
        return self.__action_stream.empty()
