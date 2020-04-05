from scape.core.dispatch import DispatchPool


def parser_rule(signal):
    def rule_func(self, *args, **kwargs):
        action_name, args = signal(self, *args, **kwargs)
        return DispatchPool.get_instance().process(action_name, args)
    return rule_func
