import abc


class BaseCommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, args):
        pass
