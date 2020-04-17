from functools import wraps


__all__ = ['action_func']


def action_func(action):
    action.__name__ = '_action_' + action.__name__
    @wraps(action)
    def fixed_action(self, *args, **kwargs):
        return action(self, *args, **kwargs)
    return fixed_action
