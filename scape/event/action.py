from scape.event.event import Event, EventFactory


__all__ = ['Action', 'ActionFactory']


class Action(Event):
    def __init__(self, name, args):
        super().__init__(name, args)
        self.__block = False

    def get_block(self):
        return self.__block

    def set_block(self, status: bool):
        self.__block = status


class ActionFactory(EventFactory):
    @classmethod
    def init_event(cls, name, args):
        return Action(name, args)
