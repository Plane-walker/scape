def transaction(action):
    def transaction_action(*args, **kwargs):
        return action(*args, **kwargs)
    return transaction_action
