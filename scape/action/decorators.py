from functools import wraps


__all__ = ['limit']


def limit(func):
    def get_action(action):
        @wraps(action)
        def fixed_action(self, *args, **kwargs):
            if func(self, *args, **kwargs):
                action(self, *args, **kwargs)
        return fixed_action
    return get_action
