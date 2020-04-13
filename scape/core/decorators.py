from scape.core.dispatch import DispatchPool
from functools import wraps


def parser_rule(signal):
    @wraps(signal)
    def rule_func(self, *args, **kwargs):
        result = signal(self, *args, **kwargs)
        if result is not None:
            action_name, args = result
            return DispatchPool.get_instance().process(action_name, args)
    return rule_func
