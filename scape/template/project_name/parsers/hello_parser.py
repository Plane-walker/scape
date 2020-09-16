from scape.core.parser import Parser
from scape.event.signal import SignalFactory
from scape.event.action import ActionFactory


class HelloParser(Parser):
    def __init__(self):
        super().__init__()
        hello_signal = SignalFactory.make('HelloSensor.say_hello')
        self.add_rule(hello_signal, self.rule)
        self.process(ActionFactory.make('Activator.init_activate', hello_signal))

    def rule(self):
        signal = self.received_signal()
        status = signal.get_status()
        if status['new'] == 'say hello':
            self.process(ActionFactory.make('Activator.deactivate', SignalFactory.make('HelloSensor.say_hello')))
            self.process(ActionFactory.make('HelloExecutor.print_to_screen', 'hello'))
            self.process(ActionFactory.make('HelloExecutor.print_to_screen', 'from escape'))
