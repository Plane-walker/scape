from scape.core.parser import Parser
from scape.action.action import CompoundAction


class ParserDemo(Parser):
    def __init__(self):
        super().__init__()
        self.add_rule('SensorDemo.signal', self.rule)

    def rule(self, args, status):
        if status['new'] == 'say hello':
            self.deactivate('SensorDemo.signal', ())
            return CompoundAction('hello')
