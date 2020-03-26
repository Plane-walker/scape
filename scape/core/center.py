class Center:
    def __init__(self):
        self.rules = {}

    def add_rule(self, *rules):
        for rule in rules:
            self.rules[rule['signal']] = rule['func']

    def process(self, signal, status):
        self.rules[signal](status)

    def try_process(self, signal, status):
        if signal in self.rules.keys():
            self.process(signal, status)
