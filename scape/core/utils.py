def func_to_str(func):
    if callable(func):
        str_group = str(func).split(' ')
        if str_group[0] == 'function':
            return str_group[1]
        return str_group[2]
    raise
