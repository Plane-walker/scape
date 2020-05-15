from scape.core.parser import Parser
from scape.signal.signal import SignalFactory
from scape.action.action import ActionFactory


class ParserDemo(Parser):
    def __init__(self):
        super().__init__()
        self.add_rule(SignalFactory.make('signal'), self.rule)
        self.process(ActionFactory.make('Activator.init_activate', (SignalFactory.make('signal'),)))

    def rule(self):
        signal = self.received_signal()
        status = signal.get_status()
        if signal.get_name() == 'signal' and status[0]['new'] == 'say' and status[1]['new'] == 'hello':
            self.process(ActionFactory.make('Activator.deactivate', (SignalFactory.make('signal'),)))
            self.process(ActionFactory.make('hello'))
