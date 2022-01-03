import functools
from contextlib import redirect_stdout
from clock_decorator import clock


#@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)


if __name__ == '__main__':
    with open('./doctest/fibo_demo_out.txt', 'a') as f:
        with redirect_stdout(f):
            print(fibonacci(10))
