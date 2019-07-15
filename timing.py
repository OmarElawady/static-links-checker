import time
def time_it(p):
    def decorator(func):
        def wrapper(*args, **kwargs):
            index = p.get_id(args[0])
            p.set_start(index, int(round(time.time() * 1000)))
            res = func(*args, **kwargs)
            p.set_end(index, int(round(time.time() * 1000)))
            return res
        return wrapper
    return decorator

