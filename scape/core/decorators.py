from scape.core.dispatch import DispatchPool
from functools import wraps


def parser_rule(signal):
    @wraps(signal)
    def rule_func(self, *args, **kwargs):
        action_name, args = signal(self, *args, **kwargs)
        return DispatchPool.get_instance().process(action_name, args)
    return rule_func
