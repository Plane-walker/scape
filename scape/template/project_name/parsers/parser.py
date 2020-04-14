from scape.core.parser import Parser


class ParserDemo(Parser):
    def __init__(self):
        super().__init__()
        self.add_rule('SensorDemo.signal', self.rule)

    def rule(self, args, status):
        self.deactivate('SensorDemo.signal', ())
        return 'ExecutorDemo.print_to_screen', (status['new'], )
