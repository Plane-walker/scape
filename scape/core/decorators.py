from scape.core.dispatch import DispatchPool
from functools import wraps


def parser_rule(signal_rule):
    @wraps(signal_rule)
    def rule_func(self, *args, **kwargs):
        if signal_rule.__name__ in self.signal_count.keys():
            self.signal_count[signal_rule.__name__][0] += 1
            self.signal_count[signal_rule.__name__][0] %= self.signal_count[signal_rule.__name__][1]
        if signal_rule.__name__ not in self.signal_count.keys() or self.signal_count[signal_rule.__name__][0] == 0:
            result = signal_rule(self, *args, **kwargs)
            if result is not None:
                action_name, args = result
                return DispatchPool.get_instance().process(action_name, args)
    return rule_func
