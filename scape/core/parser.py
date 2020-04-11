import importlib


class Parser:
    def __init__(self):
        self.rules = {}

    def add_rule(self, signal, rule):
        self.rules[signal] = rule


class ParserPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __init__(self, parsers):
        self.parsers = {}
        self.rules = {}
        for parser in parsers:
            module, parser = parser.rsplit('.', 1)
            module = importlib.import_module(module)
            parser = getattr(module, parser)()
            self.parsers[parser.__class__.__name__] = parser
            self.rules.update(parser.rules)

    def process(self, class_name, func_name, args, old_status, new_status):
        index_name = class_name + '.' + func_name
        if (index_name, args) in self.rules.keys():
            self.rules[(index_name, args)](args, {'old': old_status, 'new': new_status})
            return
        if index_name in self.rules.keys():
            self.rules[index_name](args, {'old': old_status, 'new': new_status})
