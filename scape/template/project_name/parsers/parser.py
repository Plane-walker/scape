from scape.core.parser import Parser
from scape.signal.signal import CompoundSignal
from scape.action.action import CompoundAction


class ParserDemo(Parser):
    def __init__(self):
        super().__init__()
        self.hello_signal = CompoundSignal('signal')
        self.add_rule(self.hello_signal, self.rule)
        self.init_activate(self.hello_signal)

    def rule(self, status):
        if status[0]['new'] == 'say' and status[1]['new'] == 'hello':
            self.deactivate(self.hello_signal)
            return CompoundAction('hello')
