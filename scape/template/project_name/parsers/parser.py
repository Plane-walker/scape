from scape.core.parser import Parser
from scape.signal.signal import SignalFactory
from scape.action.action import ActionFactory


class ParserDemo(Parser):
    def __init__(self):
        super().__init__()
        self.add_rule(SignalFactory.make('signal'), self.rule)
        self.init_activate(SignalFactory.make('signal'))

    def rule(self, status):
        if status[0]['new'] == 'say' and status[1]['new'] == 'hello':
            self.deactivate(SignalFactory.make('signal'))
            return ActionFactory.make('hello')
