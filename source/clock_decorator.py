import functools
import time


def clock(func):
    """
        Декоратор functools.wraps копирует аргументы
        декорируемой функции.
    """
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_list = []
        if args:
            arg_list.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = [f'{k}={w}' for k, w in sorted(kwargs.items())]
            arg_list.append(', '.join(pairs))
        arg_string = ', '.join(arg_list)
        print(f'[{elapsed:0.8f}] {name}({arg_string} -> {result})')     # [0.00000120] factorial(1 -> 1)
        return result
    return clocked
